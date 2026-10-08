"use client";

import * as React from "react";
import { motion, useScroll, useSpring, useTransform } from "framer-motion";

export function ScrollProgress() {
  const { scrollYProgress, scrollY } = useScroll();
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 400,
    damping: 30,
    restDelta: 0.001,
  });

  const [visible, setVisible] = React.useState(false);

  React.useEffect(() => {
    return scrollY.on("change", (latest) => {
      setVisible(latest > 60);
    });
  }, [scrollY]);

  if (!visible) return null;

  return (
    <motion.div
      className="fixed top-0 left-0 right-0 z-50 h-[2px] bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-500 origin-left"
      style={{ scaleX }}
    />
  );
}
