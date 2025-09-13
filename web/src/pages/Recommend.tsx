import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { postRecommend, type RecItem } from "../lib/api";
import ArticleCard from "../components/ArticleCard";
import { motion } from 'framer-motion';
import { FiUser, FiSettings, FiStar, FiList } from 'react-icons/fi';
import {
  GlassCard,
  FormContainer,
  SearchButton,
  LoadingCard,
  LoadingTextPlaceholder,
  EmptyStateContainer,
  EmptyStateIcon,
  EmptyStateTitle,
  EmptyStateMessage,
  SectionHeader,
  SectionTitle,
  SectionSubtitle
} from '../components/ui/StyledComponents';
import styled from 'styled-components';

const FormGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

const Label = styled.label`
  font-weight: 600;
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Input = styled(motion.input)`
  padding: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 1rem;
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

const Select = styled.select`
  padding: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  
  &:focus {
    outline: none;
    border-color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.1);
  }

  option {
    background: #667eea;
    color: white;
  }
`;

const ResultsHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
`;

const Badge = styled.span`
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  backdrop-filter: blur(10px);
`;

export default function Recommend() {
  const [userId, setUserId] = useState("U13740");
  const [numRecs, setNumRecs] = useState(10);
  
  const rec = useMutation({ 
    mutationFn: () => postRecommend(userId, numRecs, ["n101", "n205"]) 
  });
  
  const items: RecItem[] = rec.data ?? [];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2
      }
    }
  };

  const LoadingSkeleton = () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '2rem', padding: '2rem' }}>
      {[...Array(numRecs)].map((_, index) => (
        <LoadingCard key={index}>
          <div style={{ padding: '1.5rem' }}>
            <LoadingTextPlaceholder style={{ height: '1rem', width: '25%', marginBottom: '1rem' }} />
            <LoadingTextPlaceholder style={{ height: '1.5rem', marginBottom: '1rem' }} />
            <LoadingTextPlaceholder style={{ height: '1rem', marginBottom: '0.5rem' }} />
            <LoadingTextPlaceholder style={{ height: '1rem', width: '60%' }} />
          </div>
        </LoadingCard>
      ))}
    </div>
  );

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Header */}
      <GlassCard
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <FormContainer style={{ textAlign: 'center', padding: '2rem' }}>
          <SectionHeader>
            <SectionTitle style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>
              <FiStar style={{ display: 'inline', marginRight: '0.5rem' }} />
              Personalized Recommendations
            </SectionTitle>
            <SectionSubtitle style={{ fontSize: '1.25rem' }}>
              Get AI-powered news recommendations tailored just for you
            </SectionSubtitle>
          </SectionHeader>
        </FormContainer>
      </GlassCard>

      {/* Configuration Panel */}
      <GlassCard
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut", delay: 0.2 }}
        style={{ marginTop: '2rem' }}
      >
        <FormContainer>
          <SectionHeader style={{ marginBottom: '2rem' }}>
            <SectionTitle style={{ fontSize: '1.5rem', display: 'flex', alignItems: 'center' }}>
              <FiSettings style={{ marginRight: '0.5rem' }} />
              Recommendation Settings
            </SectionTitle>
          </SectionHeader>
          
          <FormGrid>
            {/* User ID Input */}
            <FormGroup>
              <Label htmlFor="userId">
                <FiUser />
                User ID
              </Label>
              <Input
                id="userId"
                type="text"
                placeholder="Enter your user ID (try: U13740, U91836, U73700)..."
                value={userId}
                onChange={e => setUserId(e.target.value)}
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              />
            </FormGroup>

            {/* Number of Recommendations */}
            <FormGroup>
              <Label htmlFor="numRecs">
                <FiList />
                Number of Recommendations
              </Label>
              <Select
                id="numRecs"
                value={numRecs}
                onChange={e => setNumRecs(Number(e.target.value))}
              >
                <option value={5}>5 articles</option>
                <option value={10}>10 articles</option>
                <option value={15}>15 articles</option>
                <option value={20}>20 articles</option>
              </Select>
            </FormGroup>
          </FormGrid>

          {/* Generate Button */}
          <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem' }}>
            <SearchButton
              onClick={() => rec.mutate()}
              disabled={!userId.trim() || rec.isPending}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
              style={{ padding: '1rem 2rem', fontSize: '1.1rem' }}
            >
              {rec.isPending ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    style={{ display: 'inline-block', marginRight: '0.5rem' }}
                  >
                    ⟳
                  </motion.div>
                  Generating Recommendations...
                </>
              ) : (
                <>
                  ✨ Get My Recommendations
                </>
              )}
            </SearchButton>
          </div>
        </FormContainer>
      </GlassCard>

      {/* Results */}
      {rec.isPending && (
        <GlassCard style={{ marginTop: '2rem' }}>
          <LoadingSkeleton />
        </GlassCard>
      )}

      {!rec.isPending && items.length > 0 && (
        <GlassCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          style={{ marginTop: '2rem' }}
        >
          <FormContainer>
            <ResultsHeader>
              <SectionHeader style={{ textAlign: 'left', margin: 0 }}>
                <SectionTitle style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
                  Recommendations for {userId}
                </SectionTitle>
              </SectionHeader>
              <Badge>
                {items.length} articles
              </Badge>
            </ResultsHeader>
            
            <motion.div 
              style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', 
                gap: '2rem',
                padding: '1rem'
              }}
              variants={containerVariants}
              initial="hidden"
              animate="visible"
            >
              {items.map((item, idx) => (
                <motion.div 
                  key={`${item.item_id}-${idx}`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: idx * 0.1 }}
                >
                  <ArticleCard item={item} />
                </motion.div>
              ))}
            </motion.div>
          </FormContainer>
        </GlassCard>
      )}

      {!rec.isPending && rec.isSuccess && items.length === 0 && (
        <GlassCard style={{ marginTop: '2rem' }}>
          <EmptyStateContainer>
            <EmptyStateIcon
              animate={{ 
                scale: [1, 1.1, 1],
                rotate: [0, 5, -5, 0]
              }}
              transition={{ 
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              🤖
            </EmptyStateIcon>
            <EmptyStateTitle>No recommendations found</EmptyStateTitle>
            <EmptyStateMessage>
              Try a different user ID or check if the user has interaction history.
            </EmptyStateMessage>
          </EmptyStateContainer>
        </GlassCard>
      )}
    </motion.div>
  );
}