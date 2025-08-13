# 🎙️ Voice-to-Action Assistant

> **AI-Powered Meeting Management Tool** - Transform your voice into actionable digital outputs! 🚀

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 Overview

The **Voice-to-Action Assistant** is an intelligent web application that revolutionizes how professionals handle meetings. Simply speak into your microphone, and watch as your words are transformed into structured action items, meeting summaries, calendar events, and todo lists! 

Perfect for:
- 🏢 **Business Professionals** - Streamline meeting documentation
- 👨‍💼 **Project Managers** - Automate task tracking
- 📚 **Students** - Convert lectures to study notes
- 🎯 **Anyone** who wants to turn speech into actionable digital content

## ✨ Features

### 🎤 **Voice Recognition**
- Real-time audio recording from microphone
- High-accuracy speech-to-text conversion using Google Speech Recognition
- Ambient noise adjustment for optimal results

### 🧠 **Intelligent Information Extraction**
- **Action Items**: Automatically identifies tasks and deadlines
- **Meeting Details**: Extracts dates, times, and duration
- **Key Points**: Highlights important discussion topics
- **Smart Parsing**: Understands natural language patterns

### 📱 **Digital Action Generation**
- 📅 **Calendar Events**: Create meetings with extracted details
- ✅ **Todo Lists**: Generate actionable task lists
- 📧 **Email Sharing**: Share key points via email
- 📄 **Meeting Summaries**: Comprehensive meeting documentation

### 💾 **Export & Integration**
- 📥 **Multiple Formats**: Markdown, JSON, TXT exports
- 🔗 **API Ready**: Easy integration with external services
- 📊 **Data Management**: Structured data handling

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Streamlit** | 1.22.0 | Web application framework |
| **SpeechRecognition** | 3.10.0 | Audio processing & speech recognition |
| **PyAudio** | 0.2.13 | Microphone input handling |
| **Pandas** | 1.5.3 | Data manipulation & analysis |
| **DateUtil** | 2.8.2 | Advanced date/time parsing |

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Microphone access
- Internet connection (for Google Speech Recognition)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/voice-assistant-app.git
   cd voice-assistant-app
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Open Your Browser**
   - Navigate to `http://localhost:8501`
   - Allow microphone access when prompted

## 📱 How to Use

### 🎙️ **Step 1: Record Audio**
- Click the **"🎙️ Start Recording"** button
- Speak clearly into your microphone
- Click **"⏹️ Stop Recording"** when finished
- Your speech will be automatically transcribed

### 🔍 **Step 2: Process & Extract**
- Click **"🔍 Process Transcript"** to analyze your speech
- The app will automatically identify:
  - 📋 Action items and deadlines
  - 📅 Meeting dates and times
  - 🎯 Key discussion points

### ⚡ **Step 3: Generate Actions**
- **Calendar Events**: Create meetings with extracted details
- **Todo Lists**: Generate actionable task lists
- **Email Sharing**: Share key points with team members

### 📊 **Step 4: Export & Save**
- Download meeting summaries in Markdown format
- Export all data as JSON for integration
- Save todo lists as text files

## 🎯 Use Cases

### 💼 **Business Meetings**
- Automatically capture action items
- Generate meeting summaries
- Create calendar events
- Share key points with stakeholders

### 📚 **Educational Settings**
- Convert lectures to structured notes
- Extract important concepts
- Create study guides
- Track assignment deadlines

### 🏠 **Personal Productivity**
- Voice-to-todo lists
- Meeting documentation
- Project planning
- Daily task management

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set Google Speech Recognition API key
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

### Customization
- Modify `action_keywords` in `extract_action_items()` for custom task detection
- Adjust `importance_keywords` in `extract_key_points()` for relevance scoring
- Customize date/time patterns in `extract_meeting_details()`

## 📁 Project Structure

```
voice-assistant-app/
├── 📄 app.py              # Main application file
├── 📋 requirements.txt    # Python dependencies
├── 📖 README.md          # This file
├── 🗂️ venv/              # Virtual environment
└── 📁 .gitignore         # Git ignore file
```

## 🚨 Troubleshooting

### Common Issues

**Microphone Not Working?**
- Ensure microphone permissions are granted
- Check if PyAudio is properly installed
- Try restarting the application

**Speech Recognition Errors?**
- Verify internet connection
- Check Google Speech Recognition service status
- Ensure clear audio input

**Installation Problems?**
- Update pip: `pip install --upgrade pip`
- Install system dependencies for PyAudio
- Use conda: `conda install pyaudio`

### PyAudio Installation Issues

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔀 Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Format code
black app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Speech Recognition** for audio processing
- **Streamlit** for the amazing web framework
- **Open Source Community** for inspiration and support

## 📞 Support

- 🐛 **Bug Reports**: [Create an Issue](https://github.com/yourusername/voice-assistant-app/issues)
- 💡 **Feature Requests**: [Submit a Feature Request](https://github.com/yourusername/voice-assistant-app/issues)
- 📧 **Email**: your.email@example.com
- 💬 **Discord**: [Join our community](https://discord.gg/yourinvite)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/voice-assistant-app&type=Date)](https://star-history.com/#yourusername/voice-assistant-app&Date)

---

<div align="center">
  <p>Made with ❤️ by [Your Name]</p>
  <p>If this project helps you, please give it a ⭐️!</p>
</div> 
