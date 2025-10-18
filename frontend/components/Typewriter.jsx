'use client'

import { motion } from "motion/react";
import { useEffect } from "react";

export default function TypewriterTextComponent({ examples, showExamples, exampleIndex, setExampleIndex }) {

    const letterDelay = 0.05;
    const boxFade = 0.125;

    const fadeDelay = 4;
    const mainFade = 0.25;

    const swapDelay = 4500;

    useEffect(() => {
        const id = setInterval(() => {
            setExampleIndex(prev => (prev + 1) % examples.length); 
        }, swapDelay);

        return () => clearInterval(id);
    });

    if (showExamples) {
        return (
            <motion.div layout className='absolute top-0 left-12 h-full w-10 z-20 pointer-events-none text-stone-400 flex items-center text-sm text-center text-nowrap align-center'>
                {examples[exampleIndex].split("").map((letter, index) => {
                    return <motion.span key={`${exampleIndex}-${index}`} className='relative'
                        initial={{ opacity: 1 }}
                        animate={{ opacity: 0 }}
                        transition={{ delay: fadeDelay, duration: mainFade, ease: "easeInOut" }}
                    >
                        <motion.span
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: index * letterDelay, duration: 0 }}
                        >
                            {letter === " " ? "\u00A0" : letter}
                        </motion.span>
                        <motion.span
                            initial={{ opacity: 0 }}
                            animate={{ opacity: [0, 1, 0] }}
                            transition={{ times: [0, 0.1, 1], delay: index * letterDelay, duration: boxFade, ease: "easeInOut" }}
                            className='absolute bottom-[3px] left-[1px] right-0 top-[3px] bg-stone-600'>
                        </motion.span>
                    </motion.span>
                })}
            </motion.div>
        )
    }
}