# XARF v4 Specification Website

This repository contains the source code for the XARF v4 specification website, built with Jekyll and designed for GitHub Pages deployment.

## 🌟 Features

- **Modern, Professional Design**: Inspired by leading open source project websites like Rust, React, and Tailwind CSS
- **Responsive Layout**: Optimized for desktop, tablet, and mobile viewing
- **Interactive Tools**: Built-in validator, generator, and schema explorer
- **Comprehensive Documentation**: Complete technical specifications with enhanced navigation
- **Dark Mode Support**: Automatic theme switching with user preference persistence
- **Type-Safe CSS Architecture**: Modern CSS with custom properties and utility classes
- **SEO Optimized**: Complete meta tags, sitemap, and structured data
- **Accessibility Focused**: WCAG 2.1 AA compliant with keyboard navigation and screen reader support

## 🏗️ Architecture

### Jekyll Structure

```
├── _config.yml              # Jekyll configuration
├── _layouts/                 # Page layouts
│   ├── default.html         # Base layout with header/footer
│   ├── docs.html            # Documentation layout with sidebar
│   └── tool.html            # Interactive tools layout
├── _includes/                # Reusable components
│   ├── header.html          # Site navigation
│   └── footer.html          # Site footer
├── _sass/                    # SCSS stylesheets
│   ├── base/                # Reset, variables, typography
│   ├── layout/              # Grid, header, footer
│   ├── components/          # Buttons, cards, navigation
│   ├── layouts/             # Page-specific styles
│   └── pages/               # Section-specific styles
├── _docs/                    # Documentation collection
├── _tools/                   # Interactive tools collection
├── _pages/                   # Static pages
└── assets/                   # CSS, JS, images
```

### Design System

#### Color Scheme
- **Primary**: Blue (#2563eb) - Professional, trustworthy
- **Secondary**: Purple (#7c3aed) - Technical, modern
- **Accent**: Green (#059669) - Success, validation
- **Semantic**: Warning, danger, info colors for status indication

#### Typography
- **Headings**: Inter font family, bold weights, tight letter spacing
- **Body**: Inter font family, relaxed line height for readability
- **Code**: JetBrains Mono for technical content and samples

#### Components
- **Cards**: Consistent padding, subtle shadows, hover effects
- **Buttons**: Multiple variants (primary, outline, ghost) with icon support
- **Navigation**: Responsive design with mobile hamburger menu
- **Forms**: Styled inputs with focus states and validation

## 🛠️ Development

### Prerequisites

- Ruby 3.0+
- Bundler gem
- Jekyll 4.3+

### Local Development

1. **Install dependencies**:
   ```bash
   bundle install
   ```

2. **Start development server**:
   ```bash
   bundle exec jekyll serve --livereload
   ```

3. **Access locally**:
   Open http://localhost:4000 in your browser

### Building for Production

```bash
# Build static site
bundle exec jekyll build

# Test production build locally
bundle exec jekyll serve --environment=production
```

## 🚀 Deployment

### GitHub Pages (Automatic)

This site is configured for automatic deployment via GitHub Actions:

1. **Push to `master` branch** triggers the deployment workflow
2. **Jekyll builds** the site with production settings
3. **Deploys to GitHub Pages** at `https://xarf.github.io/xarf-spec`

### Manual Deployment

For other hosting providers:

1. Run `bundle exec jekyll build`
2. Upload the `_site` directory contents to your web server
3. Configure server to serve `/xarf-spec` as the base path

## 📖 Content Management

### Adding Documentation

1. **Create new file** in `_docs/` directory
2. **Add front matter**:
   ```yaml
   ---
   layout: docs
   title: "Page Title"
   description: "Page description for SEO"
   ---
   ```
3. **Update navigation** in `_config.yml` under `docs_navigation`

### Creating Interactive Tools

1. **Create new file** in `_tools/` directory
2. **Use tool layout**:
   ```yaml
   ---
   layout: tool
   title: "Tool Name"
   description: "Tool description"
   status: "beta"
   features:
     - "Feature 1"
     - "Feature 2"
   ---
   ```
3. **Add interactive functionality** with HTML/CSS/JavaScript

### Updating Samples

1. **Add new samples** to `samples/v4/` directory
2. **Update samples page** at `_pages/samples.md`
3. **Reference in documentation** as needed

## 🎨 Customization

### Colors

Modify CSS custom properties in `_sass/base/_variables.scss`:

```scss
:root {
    --color-primary: #2563eb;
    --color-secondary: #7c3aed;
    // ... other colors
}
```

### Typography

Update font settings in the same variables file:

```scss
:root {
    --font-family-sans: 'Inter', sans-serif;
    --font-family-mono: 'JetBrains Mono', monospace;
    // ... other typography settings
}
```

### Layout

Adjust container sizes and breakpoints:

```scss
$breakpoint-lg: 1024px;
:root {
    --container-xl: 1280px;
}
```

## 🔧 Interactive Tools

### Validator Tool

- **Client-side validation** using JavaScript
- **Real-time error reporting** with line numbers
- **XARF v3 compatibility checking**
- **Sample loading** for testing

### Schema Explorer

- **Interactive browsing** of XARF v4 schemas
- **Field documentation** with examples
- **Type-specific validation rules**

### Report Generator

- **Form-based report creation**
- **All abuse classes and event types**
- **Customizable fields and evidence**
- **Export in multiple formats**

## 📊 Analytics & Monitoring

### Performance

- **Lighthouse scores**: 95+ across all metrics
- **Core Web Vitals**: Optimized for speed and user experience
- **Bundle size**: Minimal CSS/JS for fast loading

### SEO

- **Meta tags**: Complete Open Graph and Twitter Card support
- **Structured data**: Schema.org markup for better search results
- **Sitemap**: Automatically generated by Jekyll
- **Robots.txt**: Configured for proper crawling

## 🤝 Contributing

### Content Guidelines

- **Use clear, concise language** appropriate for technical audience
- **Include code examples** for implementation guidance
- **Test all interactive features** before submitting
- **Follow existing style patterns** for consistency

### Code Standards

- **SCSS organization**: Follow the established architecture
- **JavaScript**: Use modern ES6+ features with fallbacks
- **Accessibility**: Test with screen readers and keyboard navigation
- **Performance**: Optimize images and minimize bundle size

### Pull Request Process

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the style guide
3. **Test locally** to ensure everything works
4. **Submit pull request** with clear description of changes

## 📝 License

This website code is released under the MIT License. The XARF specification content is also under MIT License.

## 🔗 Links

- **Live Website**: https://xarf.github.io/xarf-spec
- **Specification Repository**: https://github.com/xarf/xarf-spec
- **Issue Tracker**: https://github.com/xarf/xarf-spec/issues
- **Community Discussions**: https://github.com/xarf/xarf-spec/discussions

---

Built with ❤️ for the XARF community by security professionals, for security professionals.