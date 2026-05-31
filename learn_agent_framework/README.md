# 安装agent framework
```bash
uv add agent-framework-azure-ai-search --prerelease=allow # 目前还是beta版
uv add agent-framework
```

# NOTES
## 新项目推荐OpenAIChatClient ，这是未来的方向。
（OpenAIChatCompletionClient，对话补全客户端虽然兼容性好，但在慢慢被抛弃）
* Agent 优先设计
* 内置 Tool Calling
* MCP 支持
* File Search
* Code Interpreter
* Image Generation
* 多模态统一
* 更好的推理模型支持
* Conversation State 支持