#!/usr/bin/env python3
"""
mac_cua.py — macOS Computer Use CLI for Antigravity (zero third-party dependencies).

Provides 1:1 equivalents to OpenAI/Codex `cua_repl` for operating Jianying Pro
(/Applications/VideoFusion-macOS.app, bundle ID: com.lemon.lvpro).
Works directly inside Antigravity's standard sandbox via native ApplicationServices & CoreGraphics!
"""
import argparse
import ctypes
import os
import subprocess
import sys
import time

# Load macOS native frameworks
cg = ctypes.cdll.LoadLibrary('/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics')
cf = ctypes.cdll.LoadLibrary('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')
ax = ctypes.cdll.LoadLibrary('/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices')

JIANYING_APP_PATH = "/Applications/VideoFusion-macOS.app"
JIANYING_BUNDLE_ID = "com.lemon.lvpro"


class CGPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]


class CGSize(ctypes.Structure):
    _fields_ = [("width", ctypes.c_double), ("height", ctypes.c_double)]


# CoreFoundation signatures
cf.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
cf.CFStringCreateWithCString.restype = ctypes.c_void_p
cf.CFStringGetLength.argtypes = [ctypes.c_void_p]
cf.CFStringGetLength.restype = ctypes.c_long
cf.CFStringGetMaximumSizeForEncoding.argtypes = [ctypes.c_long, ctypes.c_uint32]
cf.CFStringGetMaximumSizeForEncoding.restype = ctypes.c_long
cf.CFStringGetCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_uint32]
cf.CFStringGetCString.restype = ctypes.c_bool
cf.CFArrayGetCount.argtypes = [ctypes.c_void_p]
cf.CFArrayGetCount.restype = ctypes.c_long
cf.CFArrayGetValueAtIndex.argtypes = [ctypes.c_void_p, ctypes.c_long]
cf.CFArrayGetValueAtIndex.restype = ctypes.c_void_p
cf.CFGetTypeID.argtypes = [ctypes.c_void_p]
cf.CFGetTypeID.restype = ctypes.c_ulong
cf.CFStringGetTypeID.argtypes = []
cf.CFStringGetTypeID.restype = ctypes.c_ulong
cf.CFArrayGetTypeID.argtypes = []
cf.CFArrayGetTypeID.restype = ctypes.c_ulong
cf.CFBooleanGetTypeID.argtypes = []
cf.CFBooleanGetTypeID.restype = ctypes.c_ulong
cf.CFBooleanGetValue.argtypes = [ctypes.c_void_p]
cf.CFBooleanGetValue.restype = ctypes.c_bool
cf.CFNumberGetTypeID.argtypes = []
cf.CFNumberGetTypeID.restype = ctypes.c_ulong
cf.CFNumberGetValue.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
cf.CFNumberGetValue.restype = ctypes.c_bool
cf.CFRelease.argtypes = [ctypes.c_void_p]
cf.CFRelease.restype = None

kCFBooleanTrue = ctypes.c_void_p.in_dll(cf, "kCFBooleanTrue")
kCFStringEncodingUTF8 = 0x08000100
kCFNumberDoubleType = 13

# AXUIElement signatures
ax.AXIsProcessTrusted.argtypes = []
ax.AXIsProcessTrusted.restype = ctypes.c_bool
ax.AXUIElementCreateApplication.argtypes = [ctypes.c_int32]
ax.AXUIElementCreateApplication.restype = ctypes.c_void_p
ax.AXUIElementCopyAttributeValue.argtypes = [
    ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)
]
ax.AXUIElementCopyAttributeValue.restype = ctypes.c_int32
ax.AXUIElementSetAttributeValue.argtypes = [
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
]
ax.AXUIElementSetAttributeValue.restype = ctypes.c_int32
ax.AXUIElementPerformAction.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
ax.AXUIElementPerformAction.restype = ctypes.c_int32
ax.AXUIElementCopyElementAtPosition.argtypes = [
    ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_void_p)
]
ax.AXUIElementCopyElementAtPosition.restype = ctypes.c_int32
ax.AXValueGetValue.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
ax.AXValueGetValue.restype = ctypes.c_bool

kAXValueCGPointType = 1
kAXValueCGSizeType = 2

# CoreGraphics signatures
cg.CGPreflightScreenCaptureAccess.argtypes = []
cg.CGPreflightScreenCaptureAccess.restype = ctypes.c_bool
cg.CGRequestScreenCaptureAccess.argtypes = []
cg.CGRequestScreenCaptureAccess.restype = ctypes.c_bool

cg.CGMainDisplayID.restype = ctypes.c_uint32
cg.CGDisplayPixelsWide.argtypes = [ctypes.c_uint32]
cg.CGDisplayPixelsWide.restype = ctypes.c_size_t
cg.CGDisplayPixelsHigh.argtypes = [ctypes.c_uint32]
cg.CGDisplayPixelsHigh.restype = ctypes.c_size_t

cg.CGEventCreate.argtypes = [ctypes.c_void_p]
cg.CGEventCreate.restype = ctypes.c_void_p
cg.CGEventGetLocation.argtypes = [ctypes.c_void_p]
cg.CGEventGetLocation.restype = CGPoint
cg.CGWarpMouseCursorPosition.argtypes = [CGPoint]
cg.CGWarpMouseCursorPosition.restype = ctypes.c_int32

cg.CGEventCreateMouseEvent.argtypes = [
    ctypes.c_void_p, ctypes.c_uint32, CGPoint, ctypes.c_uint32
]
cg.CGEventCreateMouseEvent.restype = ctypes.c_void_p
cg.CGEventCreateKeyboardEvent.argtypes = [
    ctypes.c_void_p, ctypes.c_uint16, ctypes.c_bool
]
cg.CGEventCreateKeyboardEvent.restype = ctypes.c_void_p
cg.CGEventSetFlags.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
cg.CGEventSetFlags.restype = None
cg.CGEventSetIntegerValueField.argtypes = [
    ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int64
]
cg.CGEventSetIntegerValueField.restype = None
cg.CGEventPost.argtypes = [ctypes.c_uint32, ctypes.c_void_p]
cg.CGEventPost.restype = None
cg.CGEventCreateScrollWheelEvent.argtypes = [
    ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32
]
cg.CGEventCreateScrollWheelEvent.restype = ctypes.c_void_p

kCGEventLeftMouseDown = 1
kCGEventLeftMouseUp = 2
kCGEventRightMouseDown = 3
kCGEventRightMouseUp = 4
kCGEventMouseMoved = 5
kCGEventLeftMouseDragged = 6
kCGMouseButtonLeft = 0
kCGMouseButtonRight = 1
kCGHIDEventTap = 0
kCGSessionEventTap = 1
kCGMouseEventClickState = 1
kCGScrollEventUnitLine = 1

kCGEventFlagMaskShift = 0x00020000
kCGEventFlagMaskControl = 0x00040000
kCGEventFlagMaskAlternate = 0x00080000
kCGEventFlagMaskCommand = 0x00100000

KEYCODES = {
    'a': 0, 's': 1, 'd': 2, 'f': 3, 'h': 4, 'g': 5, 'z': 6, 'x': 7, 'c': 8, 'v': 9,
    'b': 11, 'q': 12, 'w': 13, 'e': 14, 'r': 15, 'y': 16, 't': 17, '1': 18, '2': 19,
    '3': 20, '4': 21, '6': 22, '5': 23, '=': 24, '9': 25, '7': 26, '-': 27, '8': 28,
    '0': 29, ']': 30, 'o': 31, 'u': 32, '[': 33, 'i': 34, 'p': 35, 'return': 36,
    'enter': 36, 'l': 37, 'j': 38, "'": 39, 'k': 40, ';': 41, '\\': 42, ',': 43,
    '/': 44, 'n': 45, 'm': 46, '.': 47, 'tab': 48, 'space': 49, '`': 50,
    'delete': 51, 'backspace': 51, 'escape': 53, 'esc': 53,
    'left': 123, 'right': 124, 'down': 125, 'up': 126,
}


def get_cursor_pos():
    ev = cg.CGEventCreate(None)
    if not ev:
        return (None, None)
    pt = cg.CGEventGetLocation(ev)
    cf.CFRelease(ev)
    return (round(pt.x, 1), round(pt.y, 1))


def cfstr(py_str: str) -> ctypes.c_void_p:
    return cf.CFStringCreateWithCString(None, py_str.encode('utf-8'), kCFStringEncodingUTF8)


def cf_to_py(val: ctypes.c_void_p):
    if not val:
        return None
    tid = cf.CFGetTypeID(val)
    if tid == cf.CFStringGetTypeID():
        length = cf.CFStringGetLength(val)
        max_size = cf.CFStringGetMaximumSizeForEncoding(length, kCFStringEncodingUTF8) + 1
        buf = ctypes.create_string_buffer(max_size)
        if cf.CFStringGetCString(val, buf, max_size, kCFStringEncodingUTF8):
            return buf.value.decode('utf-8', errors='replace')
        return ""
    elif tid == cf.CFBooleanGetTypeID():
        return bool(cf.CFBooleanGetValue(val))
    elif tid == cf.CFNumberGetTypeID():
        d = ctypes.c_double()
        if cf.CFNumberGetValue(val, kCFNumberDoubleType, ctypes.byref(d)):
            return d.value
        return None
    return None


def ax_get_attr(elem: ctypes.c_void_p, attr_name: str) -> ctypes.c_void_p:
    attr_cf = cfstr(attr_name)
    out = ctypes.c_void_p()
    err = ax.AXUIElementCopyAttributeValue(elem, attr_cf, ctypes.byref(out))
    cf.CFRelease(attr_cf)
    if err == 0 and out.value:
        return out.value
    return None


def ax_set_bool_true(elem: ctypes.c_void_p, attr_name: str) -> int:
    attr_cf = cfstr(attr_name)
    err = ax.AXUIElementSetAttributeValue(elem, attr_cf, kCFBooleanTrue)
    cf.CFRelease(attr_cf)
    return err


def ax_perform_action(elem: ctypes.c_void_p, action_name: str = "AXPress") -> int:
    act_cf = cfstr(action_name)
    err = ax.AXUIElementPerformAction(elem, act_cf)
    cf.CFRelease(act_cf)
    return err


def ax_get_str(elem: ctypes.c_void_p, attr_name: str):
    val = ax_get_attr(elem, attr_name)
    if not val:
        return None
    res = cf_to_py(val)
    cf.CFRelease(val)
    return res


def ax_get_point(elem: ctypes.c_void_p):
    val = ax_get_attr(elem, "AXPosition")
    if not val:
        return None
    pt = CGPoint()
    ok = ax.AXValueGetValue(val, kAXValueCGPointType, ctypes.byref(pt))
    cf.CFRelease(val)
    return (round(pt.x, 1), round(pt.y, 1)) if ok else None


def ax_get_size(elem: ctypes.c_void_p):
    val = ax_get_attr(elem, "AXSize")
    if not val:
        return None
    sz = CGSize()
    ok = ax.AXValueGetValue(val, kAXValueCGSizeType, ctypes.byref(sz))
    cf.CFRelease(val)
    return (round(sz.width, 1), round(sz.height, 1)) if ok else None


def ax_get_children(elem: ctypes.c_void_p, attr_name="AXChildren"):
    val = ax_get_attr(elem, attr_name)
    if not val:
        return None
    if cf.CFGetTypeID(val) != cf.CFArrayGetTypeID():
        cf.CFRelease(val)
        return None
    count = cf.CFArrayGetCount(val)
    items = []
    for i in range(count):
        child = cf.CFArrayGetValueAtIndex(val, i)
        if child:
            items.append(child)
    return items, val


def dump_ax_tree(elem, depth=0, max_depth=12, filter_text=None, bbox=None, include_menubar=False, lines=None):
    if lines is None:
        lines = []
    if depth > max_depth or len(lines) > 1500:
        return lines

    role = ax_get_str(elem, "AXRole") or "Unknown"
    if role == "AXMenuBar" and not include_menubar:
        return lines

    subrole = ax_get_str(elem, "AXSubrole")
    title = ax_get_str(elem, "AXTitle")
    desc = ax_get_str(elem, "AXDescription")
    val = ax_get_str(elem, "AXValue")
    ident = ax_get_str(elem, "AXIdentifier")
    enabled = ax_get_str(elem, "AXEnabled")
    selected = ax_get_str(elem, "AXSelected")
    pos = ax_get_point(elem)
    size = ax_get_size(elem)

    in_bbox = True
    if bbox and pos and size:
        bx1, by1, bx2, by2 = bbox
        cx = pos[0] + size[0] / 2.0
        cy = pos[1] + size[1] / 2.0
        if not (bx1 <= cx <= bx2 and by1 <= cy <= by2):
            in_bbox = False

    parts = [f"[{role}{('/' + str(subrole)) if subrole else ''}]"]
    if title not in (None, ""):
        parts.append(f'title="{title}"')
    if desc not in (None, ""):
        parts.append(f'desc="{desc}"')
    if val not in (None, ""):
        val_str = str(val).replace('\n', ' ')
        if len(val_str) > 80:
            val_str = val_str[:77] + "..."
        parts.append(f'value="{val_str}"')
    if ident not in (None, ""):
        parts.append(f'id="{ident}"')
    if selected is True:
        parts.append("SELECTED")
    if enabled is False:
        parts.append("disabled")
    if pos and size:
        cx = round(pos[0] + size[0] / 2.0, 1)
        cy = round(pos[1] + size[1] / 2.0, 1)
        parts.append(f"rect=({pos[0]},{pos[1]},{size[0]},{size[1]}) center=({cx},{cy})")

    line = ("  " * depth) + " ".join(parts)
    if in_bbox and (not filter_text or (filter_text.lower() in line.lower())):
        lines.append(line)

    res = ax_get_children(elem, "AXChildren")
    if res is not None:
        children, arr_ref = res
        for c in children:
            dump_ax_tree(c, depth + 1, max_depth, filter_text, bbox, include_menubar, lines)
        cf.CFRelease(arr_ref)
    return lines


def find_and_press_ax(elem, keyword: str, depth=0, max_depth=12, include_menubar=True) -> bool:
    if depth > max_depth:
        return False
    role = ax_get_str(elem, "AXRole") or ""
    if role == "AXMenuBar" and not include_menubar:
        return False
    title = ax_get_str(elem, "AXTitle") or ""
    desc = ax_get_str(elem, "AXDescription") or ""
    val = str(ax_get_str(elem, "AXValue") or "")
    ident = ax_get_str(elem, "AXIdentifier") or ""
    combined = f"{title} | {desc} | {val} | {ident}"
    if keyword.lower() in combined.lower():
        err = ax_perform_action(elem, "AXPress")
        pos = ax_get_point(elem)
        size = ax_get_size(elem)
        print(f"AXPress on [{role}] '{combined}' pos={pos} size={size} -> err={err}")
        if err == 0:
            return True

    res = ax_get_children(elem, "AXChildren")
    if res is not None:
        children, arr_ref = res
        for c in children:
            if find_and_press_ax(c, keyword, depth + 1, max_depth, include_menubar):
                cf.CFRelease(arr_ref)
                return True
        cf.CFRelease(arr_ref)
    return False


def get_jianying_pid():
    out = subprocess.run(
        ['pgrep', '-f', '/Applications/VideoFusion-macOS.app/Contents/MacOS/VideoFusion-macOS'],
        capture_output=True, text=True
    )
    pids = [int(x.strip()) for x in out.stdout.splitlines() if x.strip().isdigit()]
    return pids[0] if pids else None


def get_display_size():
    did = cg.CGMainDisplayID()
    return int(cg.CGDisplayPixelsWide(did)), int(cg.CGDisplayPixelsHigh(did))


objc = ctypes.cdll.LoadLibrary('/usr/lib/libobjc.A.dylib')
objc.objc_getClass.argtypes = [ctypes.c_char_p]
objc.objc_getClass.restype = ctypes.c_void_p
objc.sel_registerName.argtypes = [ctypes.c_char_p]
objc.sel_registerName.restype = ctypes.c_void_p

# Load AppKit so NSRunningApplication class is registered
ctypes.cdll.LoadLibrary('/System/Library/Frameworks/AppKit.framework/AppKit')


def activate_pid_via_objc(pid: int):
    cls = objc.objc_getClass(b"NSRunningApplication")
    sel_with_pid = objc.sel_registerName(b"runningApplicationWithProcessIdentifier:")
    msg_pid = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int32)(
        ("objc_msgSend", objc)
    )
    ns_app = msg_pid(cls, sel_with_pid, int(pid))
    if ns_app:
        sel_act = objc.sel_registerName(b"activateWithOptions:")
        msg_act = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong)(
            ("objc_msgSend", objc)
        )
        # 3 = NSApplicationActivateAllWindows | NSApplicationActivateIgnoringOtherApps
        msg_act(ns_app, sel_act, 3)


def bring_to_front(force: bool = False):
    pid = get_jianying_pid()
    if not pid:
        return None
    app_elem = ax.AXUIElementCreateApplication(pid)
    is_front = ax_get_str(app_elem, "AXFrontmost")
    if force or not is_front:
        try:
            activate_pid_via_objc(pid)
        except Exception:
            pass
        ax_set_bool_true(app_elem, "AXFrontmost")
        res = ax_get_children(app_elem, "AXWindows")
        if res is not None:
            wins, arr_ref = res
            for w in reversed(wins):
                ax_perform_action(w, "AXRaise")
                ax_set_bool_true(w, "AXMain")
            cf.CFRelease(arr_ref)
        time.sleep(0.2)
    cf.CFRelease(app_elem)
    return pid


def cmd_check_permissions(prompt=False):
    ax_ok = bool(ax.AXIsProcessTrusted())
    sc_ok = bool(cg.CGPreflightScreenCaptureAccess())
    print(f"Accessibility (AXIsProcessTrusted): {ax_ok}")
    print(f"Screen Recording (CGPreflightScreenCaptureAccess): {sc_ok}")
    if ax_ok and sc_ok:
        print("STATUS: All required macOS permissions are GRANTED.")
        return

    if prompt:
        if not sc_ok:
            cg.CGRequestScreenCaptureAccess()
        print("Please enable Screen Recording for Antigravity in System Settings -> Privacy & Security.")


def cmd_list_apps():
    pid = get_jianying_pid()
    w, h = get_display_size()
    print(f"Display logical size: {w}x{h}")
    print(f"Jianying Pro ({JIANYING_APP_PATH}, {JIANYING_BUNDLE_ID}) main PID: {pid}")
    print(f"AXIsProcessTrusted: {bool(ax.AXIsProcessTrusted())}")
    print(f"Current cursor: {get_cursor_pos()}")


def cmd_activate():
    pid = get_jianying_pid()
    if not pid:
        subprocess.run(['open', '-a', JIANYING_APP_PATH], check=True)
        for _ in range(15):
            time.sleep(0.5)
            pid = get_jianying_pid()
            if pid:
                break
    if not pid:
        print("ERROR: Failed to find or launch Jianying Pro.")
        sys.exit(1)

    bring_to_front(force=True)
    time.sleep(0.3)
    print(f"Activated Jianying Pro via NSRunningApplication & AXFrontmost (PID: {pid})")


def parse_bbox(bbox_str):
    if not bbox_str:
        return None
    parts = [float(x.strip()) for x in bbox_str.split(',')]
    if len(parts) != 4:
        raise ValueError("bbox must be x1,y1,x2,y2")
    return tuple(parts)


def cmd_ax_state(filter_text=None, bbox_str=None, max_depth=12, include_menubar=False, head=None):
    pid = get_jianying_pid()
    if not pid:
        print("ERROR: Jianying Pro is not running. Run `activate` first.")
        return

    bbox = parse_bbox(bbox_str)
    app_elem = ax.AXUIElementCreateApplication(pid)
    lines = dump_ax_tree(
        app_elem, depth=0, max_depth=max_depth,
        filter_text=filter_text, bbox=bbox, include_menubar=include_menubar
    )
    cf.CFRelease(app_elem)

    total = len(lines)
    if head and head > 0:
        lines = lines[:head]
    print(f"=== AX Tree for PID {pid} (showing {len(lines)}/{total} nodes, max_depth={max_depth}) ===")
    for line in lines:
        print(line)


def cmd_ax_press(keyword: str, include_menubar=True):
    pid = bring_to_front()
    if not pid:
        print("ERROR: Jianying Pro is not running.")
        return
    app_elem = ax.AXUIElementCreateApplication(pid)
    ok = find_and_press_ax(app_elem, keyword, include_menubar=include_menubar)
    cf.CFRelease(app_elem)
    if not ok:
        print(f"AXPress did not find/succeed for keyword: {keyword}")


def cmd_screenshot(out_path: str, rect_str: str = None):
    bring_to_front()
    time.sleep(0.2)
    w, h = get_display_size()
    out_abs = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)
    if rect_str:
        parts = [int(float(v.strip())) for v in rect_str.split(',')]
        if len(parts) != 4:
            raise ValueError("--rect must be x,y,w,h")
        rx, ry, rw, rh = parts
        subprocess.run(['screencapture', '-x', '-R', f"{rx},{ry},{rw},{rh}", out_abs], check=True)
        subprocess.run(
            ['sips', '-z', str(rh), str(rw), out_abs],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        print(f"Region screenshot saved: {out_abs} (logical offset=({rx},{ry}), size={rw}x{rh})")
    else:
        subprocess.run(['screencapture', '-x', out_abs], check=True)
        subprocess.run(
            ['sips', '-z', str(h), str(w), out_abs],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        print(f"Full screenshot saved: {out_abs} (1:1 logical size: {w}x{h})")


def mouse_move(x: float, y: float):
    pt = CGPoint(x, y)
    cg.CGWarpMouseCursorPosition(pt)
    ev = cg.CGEventCreateMouseEvent(None, kCGEventMouseMoved, pt, kCGMouseButtonLeft)
    cg.CGEventPost(kCGHIDEventTap, ev)
    cf.CFRelease(ev)


def mouse_click(x: float, y: float, button="left", count=1):
    bring_to_front()
    pt = CGPoint(x, y)
    mouse_move(x, y)
    time.sleep(0.08)
    if button == "right":
        down_type, up_type, btn = kCGEventRightMouseDown, kCGEventRightMouseUp, kCGMouseButtonRight
    else:
        down_type, up_type, btn = kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGMouseButtonLeft

    for i in range(1, count + 1):
        ev_down = cg.CGEventCreateMouseEvent(None, down_type, pt, btn)
        cg.CGEventSetIntegerValueField(ev_down, kCGMouseEventClickState, i)
        cg.CGEventPost(kCGHIDEventTap, ev_down)
        cf.CFRelease(ev_down)
        time.sleep(0.06)
        ev_up = cg.CGEventCreateMouseEvent(None, up_type, pt, btn)
        cg.CGEventSetIntegerValueField(ev_up, kCGMouseEventClickState, i)
        cg.CGEventPost(kCGHIDEventTap, ev_up)
        cf.CFRelease(ev_up)
        if i < count:
            time.sleep(0.06)
    print(f"Mouse {button}-click (count={count}) at ({x}, {y}) -> actual cursor: {get_cursor_pos()}")


def mouse_drag(x1: float, y1: float, x2: float, y2: float, duration=0.6, steps=30):
    bring_to_front()
    p1 = CGPoint(x1, y1)
    mouse_move(x1, y1)
    time.sleep(0.1)
    ev_down = cg.CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, p1, kCGMouseButtonLeft)
    cg.CGEventPost(kCGHIDEventTap, ev_down)
    cf.CFRelease(ev_down)
    time.sleep(0.1)
    for i in range(1, steps + 1):
        t = i / float(steps)
        cx = x1 + (x2 - x1) * t
        cy = y1 + (y2 - y1) * t
        pt = CGPoint(cx, cy)
        cg.CGWarpMouseCursorPosition(pt)
        ev_drag = cg.CGEventCreateMouseEvent(None, kCGEventLeftMouseDragged, pt, kCGMouseButtonLeft)
        cg.CGEventPost(kCGHIDEventTap, ev_drag)
        cf.CFRelease(ev_drag)
        time.sleep(duration / steps)
    time.sleep(0.1)
    p2 = CGPoint(x2, y2)
    ev_up = cg.CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, p2, kCGMouseButtonLeft)
    cg.CGEventPost(kCGHIDEventTap, ev_up)
    cf.CFRelease(ev_up)
    print(f"Mouse dragged from ({x1}, {y1}) to ({x2}, {y2}) -> actual cursor: {get_cursor_pos()}")


def mouse_scroll(x: float, y: float, dy: int):
    bring_to_front()
    mouse_move(x, y)
    time.sleep(0.08)
    ev = cg.CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitLine, 1, int(dy))
    cg.CGEventPost(kCGHIDEventTap, ev)
    cf.CFRelease(ev)
    print(f"Mouse scrolled dy={dy} at ({x}, {y})")


def send_key(combo: str, focus_first=True):
    if focus_first:
        bring_to_front()
    parts = [p.strip().lower() for p in combo.split('+')]
    flags = 0
    key_name = parts[-1]
    for mod in parts[:-1]:
        if mod in ('cmd', 'command', 'super', 'meta'):
            flags |= kCGEventFlagMaskCommand
        elif mod in ('shift',):
            flags |= kCGEventFlagMaskShift
        elif mod in ('alt', 'option', 'opt'):
            flags |= kCGEventFlagMaskAlternate
        elif mod in ('ctrl', 'control'):
            flags |= kCGEventFlagMaskControl

    if key_name not in KEYCODES:
        raise ValueError(f"Unknown key: {key_name}. Supported: {sorted(KEYCODES.keys())}")
    kc = KEYCODES[key_name]
    ev_down = cg.CGEventCreateKeyboardEvent(None, kc, True)
    if flags:
        cg.CGEventSetFlags(ev_down, flags)
    cg.CGEventPost(kCGHIDEventTap, ev_down)
    cf.CFRelease(ev_down)
    time.sleep(0.05)
    ev_up = cg.CGEventCreateKeyboardEvent(None, kc, False)
    if flags:
        cg.CGEventSetFlags(ev_up, flags)
    cg.CGEventPost(kCGHIDEventTap, ev_up)
    cf.CFRelease(ev_up)
    print(f"Sent key combo: {combo}")


def paste_text(text: str, select_all_first=True, press_enter=False):
    bring_to_front()
    proc = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    proc.communicate(input=text.encode('utf-8'))
    time.sleep(0.08)
    if select_all_first:
        send_key('cmd+a', focus_first=False)
        time.sleep(0.1)
    send_key('cmd+v', focus_first=False)
    time.sleep(0.2)
    if press_enter:
        send_key('return', focus_first=False)
    print(f"Pasted UTF-8 text ({len(text)} chars): {text}")


def add_post_args(p):
    p.add_argument("--wait", type=float, default=0.8, help="Wait seconds before post-inspect")
    p.add_argument("--ax", action="store_true", help="Dump AX tree after action")
    p.add_argument("--ax-depth", type=int, default=12, help="Max AX depth for --ax")
    p.add_argument("--ax-filter", default=None, help="Filter AX output by keyword")
    p.add_argument("--ax-bbox", default=None, help="Filter AX output by x1,y1,x2,y2 bounding box")
    p.add_argument("--shot", default=None, help="Save 1:1 logical screenshot to path after action")
    p.add_argument("--shot-rect", default=None, help="Optional x,y,w,h crop rect for --shot")


def cmd_probe(x1: float, y1: float, x2: float, y2: float, step: float = 15.0):
    pid = get_jianying_pid()
    if not pid:
        print("ERROR: Jianying Pro not running")
        return
    app_elem = ax.AXUIElementCreateApplication(pid)
    y = y1
    while y <= y2:
        x = x1
        while x <= x2:
            out = ctypes.c_void_p()
            err = ax.AXUIElementCopyElementAtPosition(app_elem, ctypes.c_float(x), ctypes.c_float(y), ctypes.byref(out))
            if err == 0 and out.value:
                role = ax_get_str(out, "AXRole")
                title = ax_get_str(out, "AXTitle")
                desc = ax_get_str(out, "AXDescription")
                val = ax_get_str(out, "AXValue")
                pos = ax_get_point(out)
                sz = ax_get_size(out)
                print(f"({x},{y}) -> [{role}] title={title} desc={desc} val={val} pos={pos} sz={sz}")
                cf.CFRelease(out)
            x += step
        y += step
    cf.CFRelease(app_elem)


def main():
    parser = argparse.ArgumentParser(description="macOS Computer Use CLI for Antigravity")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_perm = sub.add_parser("check-permissions")
    p_perm.add_argument("--prompt", action="store_true", help="Request Screen Recording permission")
    add_post_args(p_perm)

    p_list = sub.add_parser("list-apps")
    add_post_args(p_list)

    p_act = sub.add_parser("activate")
    add_post_args(p_act)

    p_ax = sub.add_parser("ax-state")
    p_ax.add_argument("--filter", default=None, help="Filter lines by substring")
    p_ax.add_argument("--bbox", default=None, help="Filter by center point inside x1,y1,x2,y2")
    p_ax.add_argument("--depth", type=int, default=12, help="Max traversal depth")
    p_ax.add_argument("--head", type=int, default=None, help="Show only first N lines")
    p_ax.add_argument("--include-menubar", action="store_true", help="Include AXMenuBar in output")
    add_post_args(p_ax)

    p_probe = sub.add_parser("probe")
    p_probe.add_argument("x1", type=float)
    p_probe.add_argument("y1", type=float)
    p_probe.add_argument("x2", type=float)
    p_probe.add_argument("y2", type=float)
    p_probe.add_argument("--step", type=float, default=15.0)
    add_post_args(p_probe)

    p_press = sub.add_parser("ax-press")
    p_press.add_argument("keyword", help="Title, desc, or id of AX element to AXPress")
    add_post_args(p_press)

    p_shot = sub.add_parser("screenshot")
    p_shot.add_argument("out", help="Output PNG file path")
    p_shot.add_argument("--rect", default=None, help="Optional logical crop x,y,w,h")
    add_post_args(p_shot)

    for name in ("click", "double-click", "right-click", "move"):
        p = sub.add_parser(name)
        p.add_argument("x", type=float)
        p.add_argument("y", type=float)
        add_post_args(p)

    p_drag = sub.add_parser("drag")
    p_drag.add_argument("x1", type=float)
    p_drag.add_argument("y1", type=float)
    p_drag.add_argument("x2", type=float)
    p_drag.add_argument("y2", type=float)
    p_drag.add_argument("--duration", type=float, default=0.6)
    add_post_args(p_drag)

    p_scroll = sub.add_parser("scroll")
    p_scroll.add_argument("x", type=float)
    p_scroll.add_argument("y", type=float)
    p_scroll.add_argument("dy", type=int, help="Scroll lines (negative = down, positive = up)")
    add_post_args(p_scroll)

    p_key = sub.add_parser("key")
    p_key.add_argument("combo", help="Key combo, e.g. cmd+shift+g, return, escape, space")
    add_post_args(p_key)

    p_paste = sub.add_parser("paste")
    p_paste.add_argument("text", help="UTF-8 string to copy and paste")
    p_paste.add_argument("--no-select", action="store_true", help="Do not send cmd+a before cmd+v")
    p_paste.add_argument("--enter", action="store_true", help="Send return after pasting")
    add_post_args(p_paste)

    args = parser.parse_args()

    if args.cmd == "check-permissions":
        cmd_check_permissions(prompt=args.prompt)
    elif args.cmd == "list-apps":
        cmd_list_apps()
    elif args.cmd == "activate":
        cmd_activate()
    elif args.cmd == "ax-state":
        cmd_ax_state(filter_text=args.filter, bbox_str=args.bbox, max_depth=args.depth, include_menubar=args.include_menubar, head=args.head)
    elif args.cmd == "probe":
        cmd_probe(args.x1, args.y1, args.x2, args.y2, step=args.step)
    elif args.cmd == "ax-press":
        cmd_ax_press(args.keyword)
    elif args.cmd == "screenshot":
        cmd_screenshot(args.out, rect_str=args.rect)
    elif args.cmd == "click":
        mouse_click(args.x, args.y, button="left", count=1)
    elif args.cmd == "double-click":
        mouse_click(args.x, args.y, button="left", count=2)
    elif args.cmd == "right-click":
        mouse_click(args.x, args.y, button="right", count=1)
    elif args.cmd == "move":
        mouse_move(args.x, args.y)
        print(f"Mouse moved to ({args.x}, {args.y}) -> actual cursor: {get_cursor_pos()}")
    elif args.cmd == "drag":
        mouse_drag(args.x1, args.y1, args.x2, args.y2, duration=args.duration)
    elif args.cmd == "scroll":
        mouse_scroll(args.x, args.y, args.dy)
    elif args.cmd == "key":
        send_key(args.combo)
    elif args.cmd == "paste":
        paste_text(args.text, select_all_first=not args.no_select, press_enter=args.enter)

    if args.ax or args.shot:
        if args.wait > 0:
            time.sleep(args.wait)
        if args.ax:
            cmd_ax_state(filter_text=args.ax_filter, bbox_str=args.ax_bbox, max_depth=args.ax_depth, head=getattr(args, 'head', None))
        if args.shot:
            cmd_screenshot(args.shot, rect_str=args.shot_rect)


if __name__ == "__main__":
    main()
