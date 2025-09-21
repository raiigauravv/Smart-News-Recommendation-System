import styled, { keyframes } from 'styled-components';
import { motion } from 'framer-motion';

// Animations
const shimmer = keyframes`
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
`;

const float = keyframes`
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
`;

// Main Container
export const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow-x: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
      radial-gradient(
        circle at 20% 80%,
        rgba(120, 119, 198, 0.3) 0%,
        transparent 50%
      ),
      radial-gradient(
        circle at 80% 20%,
        rgba(255, 119, 198, 0.3) 0%,
        transparent 50%
      );
    pointer-events: none;
  }
`;

// Header with glassmorphism
export const Header = styled(motion.header)`
  padding: 2rem 2rem 1rem;
  text-align: center;
  position: relative;
  z-index: 10;
`;

export const Title = styled(motion.h1)`
  font-size: 3.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-family: 'Poppins', sans-serif;
  letter-spacing: -0.02em;
  text-shadow: 0 4px 20px rgba(255, 255, 255, 0.1);

  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

export const Subtitle = styled(motion.p)`
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
`;

// Tab Navigation
export const TabContainer = styled.div`
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
  padding: 0 2rem;
`;

export const TabWrapper = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
`;

export const TabButton = styled(motion.button)<{ isActive: boolean }>`
  padding: 14px 28px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;

  background: ${props =>
    props.isActive
      ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      : 'transparent'};
  color: ${props => (props.isActive ? '#ffffff' : 'rgba(255, 255, 255, 0.7)')};
  box-shadow: ${props =>
    props.isActive ? '0 4px 20px rgba(102, 126, 234, 0.4)' : 'none'};

  &:hover {
    background: ${props =>
      props.isActive
        ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        : 'rgba(255, 255, 255, 0.1)'};
    color: #ffffff;
    transform: translateY(-2px);
  }

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent
    );
    transition: left 0.5s;
  }

  &:hover::before {
    left: 100%;
  }
`;

// Content Container
export const ContentContainer = styled(motion.div)`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
  position: relative;
  z-index: 5;
`;

// Glass Card
export const GlassCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.5),
      transparent
    );
  }
`;

// Article Cards
export const ArticleGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  padding: 2rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    padding: 1rem;
    gap: 1rem;
  }
`;

export const ArticleCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  overflow: hidden;
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.1),
    0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;

  &:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow:
      0 20px 40px rgba(0, 0, 0, 0.15),
      0 4px 8px rgba(0, 0, 0, 0.1);
  }

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  &:hover::before {
    opacity: 1;
  }
`;

export const ArticleImage = styled.div<{ bgImage?: string }>`
  width: 100%;
  height: 200px;
  background: ${props =>
    props.bgImage
      ? `linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%), url(${props.bgImage})`
      : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
  background-size: cover;
  background-position: center;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.1), transparent);
  }
`;

export const ArticleContent = styled.div`
  padding: 1.5rem;
`;

export const ArticleTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.75rem;
  line-height: 1.4;
  font-family: 'Poppins', sans-serif;

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;

export const ArticleAbstract = styled.p`
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1rem;

  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;

export const ArticleMeta = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
`;

export const MetaInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #888;
  font-size: 0.85rem;
  font-weight: 500;
`;

export const CategoryBadge = styled.span`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

// Form Components
export const FormContainer = styled.div`
  padding: 2rem;
`;

export const SearchContainer = styled.div`
  margin-bottom: 2rem;
`;

export const SearchInput = styled(motion.input)`
  width: 100%;
  padding: 1rem 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 1.1rem;
  font-weight: 500;

  &::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }

  &:focus {
    outline: none;
    border-color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.1);
  }
`;

export const SearchButton = styled(motion.button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  padding: 1rem 2rem;
  border-radius: 16px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6);
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

// Loading States
export const LoadingCard = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
`;

export const LoadingShimmer = styled.div`
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 1000px 100%;
  animation: ${shimmer} 1.5s infinite;
`;

export const LoadingImagePlaceholder = styled(LoadingShimmer)`
  width: 100%;
  height: 200px;
`;

export const LoadingTextPlaceholder = styled(LoadingShimmer)`
  height: 1rem;
  border-radius: 4px;
  margin-bottom: 0.5rem;

  &:last-child {
    width: 60%;
  }
`;

// Error States
export const ErrorContainer = styled.div`
  text-align: center;
  padding: 3rem 2rem;
  color: rgba(255, 255, 255, 0.8);
`;

export const ErrorTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #ff6b6b;
`;

export const ErrorMessage = styled.p`
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
`;

// Empty States
export const EmptyStateContainer = styled.div`
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.8);
`;

export const EmptyStateIcon = styled(motion.div)`
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: ${float} 3s ease-in-out infinite;
`;

export const EmptyStateTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: white;
`;

export const EmptyStateMessage = styled.p`
  font-size: 1rem;
  line-height: 1.6;
`;

// Floating Action Elements
export const FloatingElement = styled(motion.div)`
  position: absolute;
  pointer-events: none;
  opacity: 0.1;
  animation: ${float} 6s ease-in-out infinite;
`;

// Section Headers
export const SectionHeader = styled(motion.div)`
  text-align: center;
  margin-bottom: 2rem;
`;

export const SectionTitle = styled.h2`
  font-size: 2rem;
  font-weight: 800;
  color: white;
  margin-bottom: 0.5rem;
  font-family: 'Poppins', sans-serif;
`;

export const SectionSubtitle = styled.p`
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  font-weight: 400;
`;

// Button variants
export const PrimaryButton = styled(motion.button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
  }

  &:active {
    transform: translateY(0);
  }
`;

export const SecondaryButton = styled(motion.button)`
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
  }
`;

export const PDFExportButton = styled(motion.button)`
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  width: fit-content;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(231, 76, 60, 0.5);
    background: linear-gradient(135deg, #c0392b 0%, #a93226 100%);
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.2);
  }

  svg {
    width: 18px;
    height: 18px;
  }
`;
