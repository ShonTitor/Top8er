import React, { lazy } from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Base from './Base';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';
import CssBaseline from '@mui/material/CssBaseline';
import ErrorBoundary from './ErrorBoundary';

const TemplateForm = lazy(() => import('./TemplateForm'));
const TemplateGamePicker = lazy(() => import('./pages/TemplateGamePicker'));
const HomePage = lazy(() => import('./pages/HomePage'));
const AboutPage = lazy(() => import('./pages/AboutPage'));
const PrivacyPage = lazy(() => import('./pages/PrivacyPage'));
const SpecialThanksPage = lazy(() => import('./pages/SpecialThanksPage'));
const ContactPage = lazy(() => import('./pages/ContactPage'));
const BlogPage = lazy(() => import('./pages/BlogPage'));
const BlogPostPage = lazy(() => import('./pages/BlogPostPage'));
const BlogCategoryPage = lazy(() => import('./pages/BlogCategoryPage'));
const BlogAuthorPage = lazy(() => import('./pages/BlogAuthorPage'));

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ErrorBoundary>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Base />}>
              <Route index element={<HomePage />} />
              <Route path="about" element={<AboutPage />} />
              <Route path="privacy" element={<PrivacyPage />} />
              <Route path="special-thanks" element={<SpecialThanksPage />} />
              <Route path="contact" element={<ContactPage />} />
              <Route path="blog" element={<BlogPage />} />
              <Route path="blog/category/:slug" element={<BlogCategoryPage />} />
              <Route path="blog/author/:username" element={<BlogAuthorPage />} />
              <Route path="blog/:slug" element={<BlogPostPage />} />
              <Route path="template/:template" element={<TemplateGamePicker />} />
              <Route path="template/:template/game/:gameName" element={<TemplateForm />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ErrorBoundary>
    </ThemeProvider>
  </React.StrictMode>
);
