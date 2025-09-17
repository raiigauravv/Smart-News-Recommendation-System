import React, { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import Home from './pages/Home';
import Recommend from './pages/Recommend';
import {
  AppContainer,
  Header,
  Title,
  Subtitle,
  TabContainer,
  TabWrapper,
  TabButton,
  ContentContainer,
  FloatingElement,
} from './components/ui/StyledComponents';
import './App.css';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'home' | 'recommend'>('home');

  return (
    <AppContainer>
      {/* Floating Background Elements */}
      <FloatingElement
        style={{ top: '10%', left: '10%', width: '300px', height: '300px' }}
        animate={{
          y: [0, -20, 0],
          rotate: [0, 180, 360],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      >
        <div
          style={{
            width: '100%',
            height: '100%',
            background:
              'linear-gradient(45deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))',
            borderRadius: '50%',
            filter: 'blur(2px)',
          }}
        />
      </FloatingElement>

      <FloatingElement
        style={{ bottom: '10%', right: '15%', width: '200px', height: '200px' }}
        animate={{
          y: [0, 25, 0],
          x: [0, -15, 0],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 2,
        }}
      >
        <div
          style={{
            width: '100%',
            height: '100%',
            background:
              'linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03))',
            borderRadius: '30% 70% 70% 30% / 30% 30% 70% 70%',
            filter: 'blur(1px)',
          }}
        />
      </FloatingElement>

      <FloatingElement
        style={{ top: '40%', right: '5%', width: '150px', height: '150px' }}
        animate={{
          rotate: [0, 360],
          scale: [1, 1.1, 1],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: 'linear',
        }}
      >
        <div
          style={{
            width: '100%',
            height: '100%',
            background:
              'linear-gradient(45deg, rgba(255, 255, 255, 0.06), transparent)',
            borderRadius: '40% 60% 60% 40% / 60% 30% 70% 40%',
            filter: 'blur(1px)',
          }}
        />
      </FloatingElement>

      {/* Header */}
      <Header
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
      >
        <Title
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, ease: 'easeOut', delay: 0.2 }}
        >
          Smart News
        </Title>
        <Subtitle
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut', delay: 0.4 }}
        >
          Discover personalized news recommendations powered by advanced AI
          technology
        </Subtitle>
      </Header>

      {/* Navigation */}
      <TabContainer>
        <TabWrapper>
          <TabButton
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut', delay: 0.6 }}
            isActive={activeTab === 'home'}
            onClick={() => setActiveTab('home')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            Trending News
          </TabButton>
          <TabButton
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut', delay: 0.7 }}
            isActive={activeTab === 'recommend'}
            onClick={() => setActiveTab('recommend')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            Personalized
          </TabButton>
        </TabWrapper>
      </TabContainer>

      {/* Content */}
      <ContentContainer>
        <AnimatePresence mode="wait">
          {activeTab === 'home' ? (
            <Home key="home" />
          ) : (
            <Recommend key="recommend" />
          )}
        </AnimatePresence>
      </ContentContainer>
    </AppContainer>
  );
};

export default App;
