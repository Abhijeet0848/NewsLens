/**
 * NewsScope – Global Motion Tokens & Easing Curves
 * Unified, tasteful animation tokens for 60fps/120fps hardware-accelerated transforms and opacity.
 */

export const ease = {
  smooth: [0.22, 1, 0.36, 1], // easeOutQuint — primary
  snappy: [0.16, 1, 0.3, 1],
  soft: [0.4, 0, 0.2, 1],
};

export const duration = {
  fast: 0.15,
  base: 0.25,
  slow: 0.4,
  reveal: 0.6,
};

export const spring = {
  gentle: { type: "spring", stiffness: 260, damping: 30 },
  snappy: { type: "spring", stiffness: 400, damping: 32 },
  bouncy: { type: "spring", stiffness: 500, damping: 25 },
  slide: { type: "spring", stiffness: 380, damping: 34 },
};

export const variants = {
  fadeUp: {
    hidden: { opacity: 0, y: 24 },
    show: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, ease: ease.smooth },
    },
    exit: {
      opacity: 0,
      y: -12,
      transition: { duration: 0.25, ease: ease.snappy },
    },
  },
  fadeIn: {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { duration: 0.5, ease: ease.smooth },
    },
    exit: {
      opacity: 0,
      transition: { duration: 0.2, ease: ease.snappy },
    },
  },
  scaleIn: {
    hidden: { opacity: 0, scale: 0.96 },
    show: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.5, ease: ease.smooth },
    },
    exit: {
      opacity: 0,
      scale: 0.96,
      transition: { duration: 0.2, ease: ease.snappy },
    },
  },
  stagger: {
    hidden: {},
    show: {
      transition: {
        staggerChildren: 0.08,
        delayChildren: 0.1,
      },
    },
  },
  staggerFast: {
    hidden: {},
    show: {
      transition: {
        staggerChildren: 0.05,
      },
    },
  },
  slideInRight: {
    hidden: { opacity: 0, x: 24 },
    show: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.5, ease: ease.smooth },
    },
  },
};

// Aliases for backwards compatibility
export const fadeUp = variants.fadeUp;
export const fadeIn = variants.fadeIn;
export const scaleIn = variants.scaleIn;
export const stagger = variants.stagger;
export const tabContentVariant = {
  initial: { opacity: 0, y: 8 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.25, ease: ease.smooth, delay: 0.04 },
  },
  exit: {
    opacity: 0,
    y: -8,
    transition: { duration: 0.15, ease: ease.snappy },
  },
};
