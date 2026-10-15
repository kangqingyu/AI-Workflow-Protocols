import AppKit
import Foundation

// CleanShot X 风格配图画框合成脚本 (macOS 原生 AppKit，零第三方依赖)
// 用法:
//   swift -module-cache-path /tmp/swift-module-cache frame_image.swift <bgPath> <srcPath> <dstPath> [innerPad] [outerPadRatio] [cropInset]

let args = CommandLine.arguments
guard args.count >= 4 else {
    fputs("Usage: swift -module-cache-path /tmp/swift-module-cache frame_image.swift <bgPath> <srcPath> <dstPath> [innerPad=18] [outerPadRatio=0.08] [cropInset=0]\n", stderr)
    exit(1)
}

let bgPath = args[1]
let srcPath = args[2]
let dstPath = args[3]
let innerPad = args.count > 4 ? CGFloat(Double(args[4]) ?? 18.0) : 18.0
let outerPadRatio = args.count > 5 ? CGFloat(Double(args[5]) ?? 0.08) : 0.08
let cropInset = args.count > 6 ? CGFloat(Double(args[6]) ?? 0.0) : 0.0

guard let bgImage = NSImage(contentsOfFile: bgPath) else {
    fputs("Error: Cannot load background image at \(bgPath)\n", stderr)
    exit(1)
}

guard let srcImg = NSImage(contentsOfFile: srcPath),
      let srcRep = srcImg.representations.first else {
    fputs("Error: Cannot load source image at \(srcPath)\n", stderr)
    exit(1)
}

let canvasW: CGFloat = 1600
let canvasH: CGFloat = 1000
let imgW = CGFloat(srcRep.pixelsWide) - cropInset * 2.0
let imgH = CGFloat(srcRep.pixelsHigh) - cropInset * 2.0

let rep = NSBitmapImageRep(
    bitmapDataPlanes: nil,
    pixelsWide: Int(canvasW),
    pixelsHigh: Int(canvasH),
    bitsPerSample: 8,
    samplesPerPixel: 4,
    hasAlpha: true,
    isPlanar: false,
    colorSpaceName: .deviceRGB,
    bytesPerRow: 0,
    bitsPerPixel: 0
)!

NSGraphicsContext.saveGraphicsState()
let ctx = NSGraphicsContext(bitmapImageRep: rep)!
NSGraphicsContext.current = ctx
ctx.imageInterpolation = .high

// 1. 铺满 16:10 背景画布 (1600x1000)
let bgRep = bgImage.representations.first
let bgW = CGFloat(bgRep?.pixelsWide ?? Int(bgImage.size.width))
let bgH = CGFloat(bgRep?.pixelsHigh ?? Int(bgImage.size.height))
let scale = max(canvasW / bgW, canvasH / bgH)
let drawBgW = bgW * scale
let drawBgH = bgH * scale
let bgX = (canvasW - drawBgW) / 2.0
let bgY = (canvasH - drawBgH) / 2.0
bgImage.draw(in: NSRect(x: bgX, y: bgY, width: drawBgW, height: drawBgH))

// 叠加一层柔和暖米白纸感滤镜 (#f1efea @ 38%)，保证背景安静托底
NSColor(calibratedRed: 241/255.0, green: 239/255.0, blue: 234/255.0, alpha: 0.38).setFill()
NSBezierPath(rect: NSRect(x: 0, y: 0, width: canvasW, height: canvasH)).fill()

// 2. 计算自适应卡片尺寸
let maxBoxW = canvasW * (1.0 - outerPadRatio * 2.0)
let maxBoxH = canvasH * (1.0 - outerPadRatio * 2.0)
let availW = maxBoxW - innerPad * 2.0
let availH = maxBoxH - innerPad * 2.0

let imgScale = min(availW / imgW, availH / imgH)
let targetImgW = round(imgW * imgScale)
let targetImgH = round(imgH * imgScale)
let cardW = targetImgW + innerPad * 2.0
let cardH = targetImgH + innerPad * 2.0
let cardX = round((canvasW - cardW) / 2.0)
let cardY = round((canvasH - cardH) / 2.0)

let cardRect = NSRect(x: cardX, y: cardY, width: cardW, height: cardH)
let cardPath = NSBezierPath(roundedRect: cardRect, xRadius: 10, yRadius: 10)

// 3. 绘制杂志感柔和阴影与暖白卡片衬底
NSGraphicsContext.saveGraphicsState()
let shadow = NSShadow()
shadow.shadowOffset = NSSize(width: 0, height: -10)
shadow.shadowBlurRadius = 32
shadow.shadowColor = NSColor(calibratedRed: 10/255.0, green: 10/255.0, blue: 11/255.0, alpha: 0.22)
shadow.set()
NSColor(calibratedRed: 252/255.0, green: 251/255.0, blue: 249/255.0, alpha: 1.0).setFill()
cardPath.fill()
NSGraphicsContext.restoreGraphicsState()

// 4. 在圆角遮罩内绘制原图
NSGraphicsContext.saveGraphicsState()
let innerRect = NSRect(x: cardX + innerPad, y: cardY + innerPad, width: targetImgW, height: targetImgH)
let innerPath = NSBezierPath(roundedRect: innerRect, xRadius: 6, yRadius: 6)
innerPath.addClip()
let fromRect = NSRect(
    x: cropInset,
    y: cropInset,
    width: srcImg.size.width - cropInset * 2.0,
    height: srcImg.size.height - cropInset * 2.0
)
srcImg.draw(in: innerRect, from: fromRect, operation: .sourceOver, fraction: 1.0)
NSGraphicsContext.restoreGraphicsState()

// 5. 极细边框收口
NSColor(calibratedRed: 10/255.0, green: 10/255.0, blue: 11/255.0, alpha: 0.08).setStroke()
cardPath.lineWidth = 1.0
cardPath.stroke()

NSGraphicsContext.restoreGraphicsState()

let dstURL = URL(fileURLWithPath: dstPath)
try FileManager.default.createDirectory(at: dstURL.deletingLastPathComponent(), withIntermediateDirectories: true)
guard let jpgData = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.92]) else {
    fputs("Error: Failed to encode JPEG\n", stderr)
    exit(1)
}
try jpgData.write(to: dstURL)
print("Generated CleanShot X frame: \(dstPath)")
