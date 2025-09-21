import { useQuery, useMutation } from "@tanstack/react-query";
import {
  fetchTrending,
  postSearch,
  fetchCategories,
  postExportPdf,
  type RecItem,
} from '../lib/api';
import ArticleCard from '../components/ArticleCard';
import { useState } from 'react';
import { motion } from 'framer-motion';
import { FiSearch, FiTrendingUp, FiArrowLeft, FiDownload } from 'react-icons/fi';
import {
  GlassCard,
  FormContainer,
  SearchContainer,
  SearchInput,
  SearchButton,
  LoadingCard,
  LoadingTextPlaceholder,
  PDFExportButton,
  EmptyStateContainer,
  EmptyStateIcon,
  EmptyStateTitle,
  EmptyStateMessage,
  SectionHeader,
  SectionTitle,
  SectionSubtitle,
  SecondaryButton,
} from '../components/ui/StyledComponents';

export default function Home() {
  const { data: trending, isLoading: trendingLoading } = useQuery({
    queryKey: ['trending'],
    queryFn: () => fetchTrending(20),
  });

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: fetchCategories,
  });

  const [q, setQ] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  const search = useMutation({
    mutationFn: () => postSearch(q, 20, selectedCategory || undefined),
    onSuccess: () => setQ(''),
  });

  const exportMutation = useMutation({
    mutationFn: async (items: RecItem[]) => {
      console.log('Exporting', items.length, 'articles to PDF...');
      const blob = await postExportPdf(items, "home_user");
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "smart_news_report.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      console.log('PDF download started successfully');
    },
    onError: (error) => {
      console.error('PDF export failed:', error);
      alert('Failed to export PDF. Please try again.');
    },
  });

  const items: RecItem[] = search.data ?? trending ?? [];
  const isSearchActive = search.data !== undefined;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const LoadingSkeleton = () => (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
        gap: '2rem',
        padding: '2rem',
      }}
    >
      {[...Array(6)].map((_, index) => (
        <LoadingCard key={index}>
          <div style={{ padding: '1.5rem' }}>
            <LoadingTextPlaceholder
              style={{ height: '1rem', width: '25%', marginBottom: '1rem' }}
            />
            <LoadingTextPlaceholder
              style={{ height: '1.5rem', marginBottom: '1rem' }}
            />
            <LoadingTextPlaceholder
              style={{ height: '1rem', marginBottom: '0.5rem' }}
            />
            <LoadingTextPlaceholder style={{ height: '1rem', width: '60%' }} />
          </div>
        </LoadingCard>
      ))}
    </div>
  );

  return (
    <motion.div variants={containerVariants} initial="hidden" animate="visible">
      {/* Hero Section */}
      <GlassCard
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
      >
        <FormContainer style={{ textAlign: 'center', padding: '3rem 2rem' }}>
          <SectionHeader>
            <SectionTitle style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>
              Discover News That Matters
            </SectionTitle>
            <SectionSubtitle
              style={{ fontSize: '1.25rem', marginBottom: '2rem' }}
            >
              AI-powered recommendations from thousands of sources
            </SectionSubtitle>
          </SectionHeader>

          {/* Search Bar */}
          <SearchContainer style={{ maxWidth: '600px', margin: '0 auto' }}>
            <div style={{ position: 'relative' }}>
              <SearchInput
                placeholder="Search for news topics, keywords, or categories (try: sports, health, finance)..."
                value={q}
                onChange={e => setQ(e.target.value)}
                onKeyPress={e =>
                  e.key === 'Enter' && q.trim() && search.mutate()
                }
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              />
              <FiSearch
                style={{
                  position: 'absolute',
                  right: '1rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  color: 'rgba(255, 255, 255, 0.6)',
                  fontSize: '1.2rem',
                }}
              />
            </div>

            {/* Category Selector */}
            {categories && categories.length > 0 && (
              <select
                value={selectedCategory}
                onChange={e => setSelectedCategory(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem',
                  marginTop: '1rem',
                  background: 'rgba(255, 255, 255, 0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: '12px',
                  color: 'white',
                  fontSize: '1rem',
                  outline: 'none',
                  cursor: 'pointer',
                }}
              >
                <option
                  value=""
                  style={{ background: '#1a1a1a', color: 'white' }}
                >
                  All Categories
                </option>
                {categories.map(category => (
                  <option
                    key={category}
                    value={category}
                    style={{ background: '#1a1a1a', color: 'white' }}
                  >
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </option>
                ))}
              </select>
            )}

            {/* Quick Category Tags */}
            <div
              style={{
                display: 'flex',
                gap: '0.5rem',
                marginTop: '1rem',
                flexWrap: 'wrap',
                justifyContent: 'center',
              }}
            >
              {['sports', 'health', 'finance', 'news', 'entertainment'].map(
                tag => (
                  <button
                    key={tag}
                    onClick={() => {
                      setQ(tag);
                      setSelectedCategory(tag);
                      setTimeout(() => search.mutate(), 100);
                    }}
                    style={{
                      padding: '0.5rem 1rem',
                      background:
                        selectedCategory === tag
                          ? 'rgba(255, 255, 255, 0.2)'
                          : 'rgba(255, 255, 255, 0.1)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '20px',
                      color: 'white',
                      fontSize: '0.875rem',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease',
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.background =
                        'rgba(255, 255, 255, 0.2)';
                      e.currentTarget.style.transform = 'scale(1.05)';
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.background =
                        selectedCategory === tag
                          ? 'rgba(255, 255, 255, 0.2)'
                          : 'rgba(255, 255, 255, 0.1)';
                      e.currentTarget.style.transform = 'scale(1)';
                    }}
                  >
                    #{tag}
                  </button>
                )
              )}
            </div>

            <SearchButton
              onClick={() => q.trim() && search.mutate()}
              disabled={!q.trim() || search.isPending}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
            >
              {search.isPending ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{
                      duration: 1,
                      repeat: Infinity,
                      ease: 'linear',
                    }}
                    style={{ display: 'inline-block', marginRight: '0.5rem' }}
                  >
                    ⟳
                  </motion.div>
                  Searching...
                </>
              ) : (
                <>
                  <FiSearch style={{ marginRight: '0.5rem' }} />
                  Search
                </>
              )}
            </SearchButton>
          </SearchContainer>

          <div style={{ display: 'flex', justifyContent: 'center', marginTop: '1rem' }}>
            <PDFExportButton
              onClick={() => exportMutation.mutate(items ?? [])}
              disabled={!items || items.length === 0 || exportMutation.isPending}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <FiDownload />
              {exportMutation.isPending ? 'Exporting...' : 'Export PDF'}
            </PDFExportButton>
          </div>
        </FormContainer>
      </GlassCard>

      {/* Results Section */}
      <GlassCard
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut', delay: 0.2 }}
        style={{ marginTop: '2rem' }}
      >
        <FormContainer>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '2rem',
            }}
          >
            <SectionHeader style={{ textAlign: 'left', margin: 0 }}>
              <SectionTitle
                style={{
                  fontSize: '2rem',
                  marginBottom: '0.5rem',
                  display: 'flex',
                  alignItems: 'center',
                }}
              >
                <FiTrendingUp style={{ marginRight: '0.5rem' }} />
                {isSearchActive ? 'Search Results' : 'Trending Stories'}
              </SectionTitle>
            </SectionHeader>

            {isSearchActive && (
              <SecondaryButton
                onClick={() => search.reset()}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.98 }}
              >
                <FiArrowLeft style={{ marginRight: '0.5rem' }} />
                Back to Trending
              </SecondaryButton>
            )}
          </div>

          {/* Loading State */}
          {(trendingLoading || search.isPending) && <LoadingSkeleton />}

          {/* Articles Grid */}
          {!trendingLoading && !search.isPending && (
            <>
              {items.length > 0 ? (
                <motion.div
                  style={{
                    display: 'grid',
                    gridTemplateColumns:
                      'repeat(auto-fill, minmax(350px, 1fr))',
                    gap: '2rem',
                    padding: '1rem',
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
              ) : (
                <EmptyStateContainer>
                  <EmptyStateIcon
                    animate={{
                      scale: [1, 1.1, 1],
                      rotate: [0, 5, -5, 0],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: 'easeInOut',
                    }}
                  >
                    📰
                  </EmptyStateIcon>
                  <EmptyStateTitle>
                    {isSearchActive
                      ? 'No articles found'
                      : 'No trending articles'}
                  </EmptyStateTitle>
                  <EmptyStateMessage>
                    {isSearchActive
                      ? 'Try different keywords or browse trending stories.'
                      : 'Check back later for the latest trends.'}
                  </EmptyStateMessage>
                </EmptyStateContainer>
              )}
            </>
          )}
        </FormContainer>
      </GlassCard>
    </motion.div>
  );
}
