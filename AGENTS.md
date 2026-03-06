# AGENTS.md

## Quick Start

```bash
# List available models
curl http://localhost:8080/v1/models

# Chat completion (Qwen3-Coder-Next)
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "unsloth/Qwen3-Coder-Next-GGUF:UD-Q4_K_XL",
    "messages": [{"role": "user", "content": "Hello"}]
  }'

# Chat completion (GPT-OSS 20b)
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "unsloth/gpt-oss-20b-GGUF:F16",
    "messages": [{"role": "user", "content": "Explain quantum mechanics"}]
  }'
```

## Server Configuration

- **Host**: localhost
- **Port**: 8080
- **GPU Setup**: 4 identical GPUs with tensor-split distribution
- **System RAM**: 128 GB
- **VRAM**: 44 GB total (~11 GB per GPU)

## Available Models

| Model | Quant | Context | GPU Layers | Use Case |
|-------|-------|---------|------------|----------|
| Unsloth Qwen3 Q4XL | UD-Q4_K_XL | 262K | 35 | Coding, agentic tasks |
| GPT-OSS 20b | F16 | 32K | Full | Reasoning, general |
| Qwen3-Coder-Next | Q5_K_M | 262K | 48 | Coding, tool use |
| Gemma 3 1b | GGUF | 8K | Full | Fast general tasks |

## Environment Variables

```bash
# GPU selection (if needed)
export CUDA_VISIBLE_DEVICES=0,1,2,3

# Server flags (pass to llama-server)
# -c, --ctx-size: Context window
# -ngl, --n-gpu-layers: GPU layers
# --tensor-split: Distribution across GPUs
```

## Model Selection Guide

**Use Qwen3 Q4XL when:**
- Coding tasks, especially long-context
- Tool calling and agentic workflows
- You need up to 262K context window

**Use GPT-OSS 20b when:**
- Reasoning and analysis
- General conversation
- 32K context is sufficient

**Use Qwen3 Q5_K_M when:**
- Coding tasks with slightly better quality than Q4
- You have enough VRAM (requires ~57GB)

**Use Gemma 3 1b when:**
- Fast, lightweight tasks
- Limited VRAM environment
- General dialogue and summarization

## Testing & Debugging

**Check server health:**
```bash
curl http://localhost:8080/health
```

**View server logs:**
- Check where tharkad server is running
- Look for CUDA OOM errors if layers too high

**Common Issues:**

1. **CUDA Out of Memory**: Reduce `n-gpu-layers` or use smaller quant
2. **Context too long**: Ensure `ctx-size` matches model's max
3. **Slow inference**: Increase `n-gpu-layers` if VRAM allows

## GPU Layer Recommendations

| Model | Max Layers | Recommended | Reason |
|-------|------------|-------------|--------|
| Qwen3 Q4XL | ~40 | 35 | 44GB VRAM limit |
| GPT-OSS 20b | ~20 | Full | F16 fits in VRAM |
| Qwen3 Q5_K_M | ~48 | 48 | Requires >57GB VRAM |
| Gemma 3 1b | ~24 | Full | Fits in minimal VRAM |

## Maintenance

**Restart server (on tharkad machine):**
```bash
# SSH to tharkad server
ssh donny@tharkad

# Restart the llama.cpp server
systemctl restart llama-server
# or however the service is managed
```

**Update models:**
- Models are served from tharkad's storage
- Download new GGUF files to tharkad: `huggingface-cli download <repo> --include "*.gguf"`
- Server picks up new models automatically (no restart needed)
- Update `hf-repo` in tharkad.ini only if changing model sources

## API Parameters

Common parameters for `/v1/chat/completions`:

```json
{
  "model": "model-name-from-list",
  "messages": [
    {"role": "user", "content": "Your prompt"}
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 4096,
  "stream": false
}
```

**Qwen3-specific recommendations:**
- Use `temperature: 1.0, top_p: 0.95, top_k: 40` for optimal coding
- Enable `tools` array for function calling
- Max tokens up to 65536 for long outputs