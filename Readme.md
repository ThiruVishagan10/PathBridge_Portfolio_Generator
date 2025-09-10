# 🌉 PathBridge Portfolio Generator

PathBridge Portfolio Generator is a **Python-based AI-powered tool** that generates professional, responsive HTML portfolios using **Google’s Gemini AI** to enhance user-provided content.  
It helps students, professionals, and developers quickly create an impressive portfolio with modern design and animations.

---

## 🚀 Project Details
- **Name:** PathBridge Portfolio Generator  
- **Purpose:** Generates professional HTML portfolios using **Gemini AI** for content enhancement  
- **Main Script:** `portfolio.py`  
- **Template:** `template_portfolio.html` (Bootstrap 5 dark theme)  
- **Sample Data:** `sample-data.json`  
- **Output:** `output/portfolio.html`  

---

## ✨ Key Features
- 📥 **Flexible Input:** Collect data interactively or load from a JSON file  
- 🤖 **AI-Powered:** Enhances descriptions & sections with **Gemini 1.5 Flash**  
- 🎨 **Modern Design:** Dark-themed, professional, responsive portfolio  
- 🖌 **Built with Bootstrap 5** for styling & layout  
- 🎬 **Smooth animations** via [AOS](https://michalsnik.github.io/aos/)  
- ⌨️ **Dynamic text effects** using [Typed.js](https://github.com/mattboldt/typed.js/)  
- 📚 **Comprehensive Sections:**
  - About  
  - Education  
  - Skills  
  - Projects  
  - Experience  
  - Certifications  

---

## 🛠 Technical Stack
- **Language:** Python 3.7+  
- **AI:** Google Generative AI (Gemini 1.5 Flash)  
- **Templating:** Jinja2  
- **Frontend:** Bootstrap 5, AOS animations, Typed.js  

---

## 📦 Dependencies
Install the following Python libraries:

```bash
pip install google-generativeai python-dotenv jinja2
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/PathBridge_Portfolio_Generator.git
cd PathBridge_Portfolio_Generator
```

### 2. Install Dependencies
```bash
pip install google-generativeai python-dotenv jinja2
```

### 3. Set up Gemini API Key
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Get your API key from:** [Google AI Studio](https://makersuite.google.com/app/apikey)

---

## 🚀 Usage

### Option 1: Using Sample Data
```bash
python portfolio.py
```
This will use the provided `sample-data.json` file to generate a portfolio.

### Option 2: Interactive Input
Modify the main section in `portfolio.py` to use `collect_user_data()` for interactive input.

### Generated Output
The portfolio will be saved as `output/portfolio.html` - open it in your browser to view!

---

## 📁 File Structure
```
PathBridge_Portfolio_Generator/
├── portfolio.py              # Main script
├── template_portfolio.html   # HTML template (dark theme)
├── sample-data.json         # Sample portfolio data
├── .env                     # API key (create this)
├── .gitignore              # Git ignore file
├── README.md               # This file
└── output/                 # Generated portfolios
    └── portfolio.html      # Your generated portfolio
```

---

## 🎨 Features in Detail

### AI Enhancement
- **Content Polishing:** Gemini AI improves all text sections
- **Professional Formatting:** Converts raw input into portfolio-ready content
- **Smart Descriptions:** Enhances project and experience descriptions

### Dark Theme Design
- **Modern Aesthetics:** Professional dark color scheme
- **Responsive Layout:** Works on all devices
- **Smooth Animations:** AOS library for scroll animations
- **Interactive Elements:** Hover effects and transitions

### Comprehensive Sections
- **About Me:** AI-generated professional summary
- **Education:** Formatted academic background
- **Skills:** Visual progress bars for technical skills
- **Projects:** Detailed project showcases
- **Experience:** Professional work history
- **Certifications:** Achievement highlights

---

## 🔧 Customization

### Modify Template
Edit `template_portfolio.html` to customize:
- Colors and styling
- Layout and sections
- Animations and effects

### Update Sample Data
Modify `sample-data.json` with your information:
```json
{
  "name": "Your Name",
  "about": "Your bio",
  "education": "Your education",
  "skills": ["Skill 1", "Skill 2"],
  "projects": ["Project 1", "Project 2"],
  "experience": ["Experience 1"],
  "certifications": ["Cert 1"]
}
```

---

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments
- **Google Gemini AI** for content enhancement
- **Bootstrap 5** for responsive design
- **AOS Library** for smooth animations
- **Typed.js** for dynamic text effects

---

## 📞 Support
If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/PathBridge_Portfolio_Generator/issues) page
2. Create a new issue with detailed information
3. Contact the maintainer

**Happy Portfolio Building! 🚀**
