# Blog LLM Project

AI-powered blog writing assistant using Llama 3.2 model.

## Features

- 🤖 Local LLM integration (Llama 3.2 1B)
- 🌐 Web-based interface
- 📊 Real-time performance metrics
- 🎨 Multiple blog types and tones
- 📱 Responsive design
- 🔧 Easy deployment with Docker

## Quick Start

1. **Run setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Start the application:**
   ```bash
   ./start.sh
   ```

3. **Access the demo:**
   - Web Interface: http://localhost:8080/demo.html
   - API Documentation: http://localhost:8000/docs

## Project Structure

```
blog-llm-project/
├── api/                 # FastAPI backend
├── frontend/           # Web interface
├── models/            # Model configurations
├── evaluation/        # Performance testing
├── docker/           # Container deployment
└── requirements.txt  # Python dependencies
```

## API Endpoints

- `POST /generate-blog` - Generate blog content
- `GET /health` - Health check
- `GET /models` - List available models

## Performance Metrics

- Generation Speed: ~2-5 tokens/second on CPU
- Memory Usage: ~2-3GB RAM
- Model Size: ~1.3GB disk space

## Deployment Options

### Local Development
```bash
./start.sh
```

### Docker Deployment
```bash
cd docker
docker-compose up --build
```

### Production Deployment
1. Use larger models (7B/13B) with GPU
2. Add authentication and rate limiting
3. Implement caching and database storage
4. Scale with load balancers

## Customization

### Adding New Blog Types
Edit `api/main.py` and add new blog types to the generation logic.

### Changing Models
```bash
ollama pull llama3.2:3b  # or other models
# Update MODEL_NAME in api/main.py
```

### Fine-tuning
1. Prepare training data in `models/training_data/`
2. Use the fine-tuning scripts in `models/fine_tune.py`
3. Update model path in configuration

## Troubleshooting

### Ollama Connection Issues
```bash
ollama serve
ollama pull llama3.2:1b
```

### Memory Issues
- Use smaller models (1B instead of 3B)
- Reduce context window size
- Close other applications

### Slow Generation
- Enable GPU acceleration if available
- Use quantized models
- Reduce target word count

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests and documentation
4. Submit pull request

## License

MIT License - see LICENSE file for details.
EOF

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run: chmod +x start.sh"
echo "2. Run: ./start.sh"
echo "3. Open: http://localhost:8080/demo.html"
echo ""
echo "Project structure created in: $(pw