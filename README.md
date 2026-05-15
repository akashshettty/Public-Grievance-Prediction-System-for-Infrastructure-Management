# Public Grievance Prediction System for Infrastructure Management

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-success.svg)

UrbanPulse AI is an enterprise-grade Smart City Intelligence Platform that transforms public grievance data into actionable infrastructure health insights.

## 🎯 Overview

This system converts historical grievance records into:
- **Geospatial Heatmaps**: Visualize problem density across the city.
- **Risk Scoring**: Area-wise risk assessment (0-100) based on multiple metrics.
- **Predictive Analytics**: ML-driven future hotspot forecasting and timelines.
- **Interactive Dashboard**: Premium React-based UI for operational monitoring.

## ✨ Key Features

### 🎨 Premium UI/UX
- Midnight blue & graphite black backgrounds with glassmorphism.
- Smooth Framer Motion animations and professional typography (Inter).
- Intelligent KPI cards, premium tables, and interactive charts.

### 🤖 AI-Driven Insights
- Auto-generated intelligence summaries.
- Predictive alerts and infrastructure degradation analysis.
- Risk escalation warnings and natural language insights.

## 📁 Project Structure
- `backend/` - Flask REST API services.
- `frontend/` - React dashboard application.
- `ml_modules/` - Machine learning training and inference scripts.
- `src/` - Data processing, feature engineering, and visualization logic.
- `data/` - Raw and processed datasets.
- `models/` - Saved ML model weights.

## 🚀 Quick Start

### Installation

```bash
# 1. Run setup script
# Windows:
setup.bat

# Linux/Mac:
bash setup.sh
```

### Running the System

**Terminal 1 - Backend (API)**
```bash
python wsgi.py
```

**Terminal 2 - Frontend**
```bash
cd frontend
npm run dev
```

## 🛠️ Technology Stack
- **Frontend**: React 18, TailwindCSS, Framer Motion, Recharts, Lucide.
- **Backend**: Flask, Pandas, NumPy, Scikit-learn.
- **Deployment**: Docker, Nginx.

## 📄 License
MIT License

---
**Made with 🚀 for Smart City Intelligence**
