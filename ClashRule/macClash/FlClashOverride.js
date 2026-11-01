/**
 * FlClash 扩展覆写脚本
 * 唯一数据源: https://github.com/kangqingyu/AI-Workflow-Protocols/tree/main/ClashRule/macClash
 */
function main(config) {
  if (!config["rule-providers"]) {
    config["rule-providers"] = {};
  }
  if (!config["rules"]) {
    config["rules"] = [];
  }

  // 动态获取当前订阅的首个代理策略组，兼容任意机场订阅并确保 GitHub Raw 稳定拉取
  const proxyGroups = config["proxy-groups"] || [];
  const defaultProxy =
    proxyGroups.length > 0 && proxyGroups[0].name
      ? proxyGroups[0].name
      : "DIRECT";

  const baseRawUrl =
    "https://raw.githubusercontent.com/kangqingyu/AI-Workflow-Protocols/main/ClashRule/macClash";

  // 1. 注入 GitHub 远程规则集数据源
  Object.assign(config["rule-providers"], {
    KqyDirect: {
      type: "http",
      behavior: "classical",
      format: "yaml",
      proxy: defaultProxy,
      url: `${baseRawUrl}/Direct.yaml`,
      path: "./ruleset/KqyDirect.yaml",
      interval: 3600,
    },
    KqyReject: {
      type: "http",
      behavior: "classical",
      format: "yaml",
      proxy: defaultProxy,
      url: `${baseRawUrl}/Reject.yaml`,
      path: "./ruleset/KqyReject.yaml",
      interval: 3600,
    },
  });

  // 2. 将自定义规则集置顶插入 rules（优先级最高）
  const customRules = [
    "RULE-SET,KqyReject,REJECT",
    "RULE-SET,KqyDirect,DIRECT",
  ];

  config["rules"] = customRules.concat(config["rules"]);

  return config;
}
