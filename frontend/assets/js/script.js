let generationStartTime;

async function generateBlog() {
    const topic = document.getElementById('topic').value.trim();
    const blogType = document.getElementById('blog-type').value;
    const wordCount = document.getElementById('word-count').value;
    const tone = document.getElementById('tone').value;
    const audience = document.getElementById('audience').value;
    
    if (!topic) {
        alert('Please enter a blog topic!');
        return;
    }
    
    const generateBtn = document.querySelector('.generate-btn');
    const output = document.getElementById('blog-output');
    const copyBtn = document.getElementById('copy-btn');
    
    // Start loading state
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating...';
    output.innerHTML = '<div class="loading"><div class="spinner"></div>Generating your blog post...</div>';
    copyBtn.style.display = 'none';
    generationStartTime = Date.now();
    
    try {
        const response = await fetch('http://localhost:8000/generate-blog', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic: topic,
                type: blogType,
                word_count: parseInt(wordCount),
                tone: tone,
                audience: audience
            })
        });
        
        
        if (response.ok) {
            const data = await response.json();
            
            // Display generated content
            output.textContent = data.content;
            copyBtn.style.display = 'block';
            
            // Update stats
            updateStats(data.content);
            
        } else {
            const errorData = await response.json();
            output.textContent = `Error: ${errorData.detail || 'Failed to generate blog post'}`;
        }
        
    } catch (error) {
        output.textContent = 'Error: Cannot connect to the API server. Please ensure the backend is running.';
        console.error('Generation error:', error);
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Blog Post';
    }
}

function updateStats(content) {
    const words = content.trim().split(/\s+/).filter(word => word.length > 0).length;
    const characters = content.length;
    const readTime = Math.ceil(words / 200); // Average reading speed
    const generationTime = (Date.now() - generationStartTime) / 1000;
    
    document.getElementById('word-count-stat').textContent = words;
    document.getElementById('char-count-stat').textContent = characters;
    document.getElementById('read-time-stat').textContent = readTime;
    document.getElementById('generation-time').textContent = generationTime.toFixed(1);
}

function copyToClipboard() {
    const output = document.getElementById('blog-output');
    const text = output.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        const copyBtn = document.getElementById('copy-btn');
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✅ Copied!';
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy to clipboard');
    });
}

// Allow Enter key to trigger generation
document.getElementById('topic').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        generateBlog();
    }
});