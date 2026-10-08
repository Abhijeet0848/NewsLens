/**
 * NewsScope – Global Motion Tokens & Easing Curves
 * Optimized for 60fps/120fps hardware-accelerated transforms and opacity.
 */

export const ease = {
  smooth: [0.22, 1, 0.36, 1], // easeOutQuint — primary
  snappy: [0.16, 1, 0.3, 1],
  soft: [0.4, 0, 0.2, 1],
  spring: { type: "spring", stiffness: 380, damping: 30 },
  bouncy: { type: "spring", stiffness: 400, damping: 25 },
};

export const fadeUp = {
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
};

export const fadeIn = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { duration: 0.5, ease: ease.smooth },
  },
  exit: {
    opacity: 0,
    transition: { duration: 0.2, ease: ease.snappy },
  },
};

export const stagger = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.05,
    },
  },
};

export const scaleIn = {
  hidden: { opacity: 0, scale: 0.94 },
  show: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.45, ease: ease.smooth },
  },
  exit: {
    opacity: 0,
    scale: 0.96,
    transition: { duration: 0.2, ease: ease.snappy },
  },
};

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
