'use client'

import { Plus } from "lucide-react";
import { motion } from "motion/react";
import { useRef, useEffect, useState } from "react";

export default function Header() {

    const containerRef = useRef(null);
    const [width, setWidth] = useState(0);

    useEffect(() => {
        if (containerRef.current) {
            setWidth(containerRef.current.scrollWidth / 2 + 3);
        }
    }, []);

    return (
        <div className="absolute top-0 left-0 w-screen z-10 p-3">
            
            <div className="flex flex-row items-center mt-1">
                <div className="flex flex-row items-center relative translate-y-[2px]">
                    <img src="eth.png" width={30} height={30} className="relative"></img>
                    <p className="text-white text-2xl font-bold relative -translate-x-[3px] -translate-y-[1px]">lens</p>
                </div>
                <div ref={containerRef} className="ml-auto w-[500px] mr-[20] overflow-hidden flex flex-row gap-2 bg-black relative opacity-0 md:opacity-100 transition-all duration-500">

                    <motion.div 
                        className="flex gap-2 w-[200%] relative"
                        animate={{
                            x: [0, -width],
                            transition: {
                                x: {
                                    duration: 15,
                                    ease: "linear",
                                    repeat: Infinity,
                                    repeatType: "loop"
                                }
                            }
                        }}
                    >

                        {
                            [...Array(2)].map((_, i) => (
                                <div key={i} className="flex gap-2">
                                    {["learn", "become great", "acheive", "grow", "discover"].map((str, key) => ( 
                                        <div
                                            key={`${i}-${key}`}
                                            className="bg-black text-white uppercase whitespace-nowrap flex flex-row items-center gap-2"
                                        >
                                            <p className="blur-[1.5px] hover:blur-[0px] transition-all ease-in-out duration-500 text-neutral-350 font-semibold">0{key} {str}</p>
                                            <p className="blur-[1.5px] relative -translate-y-[1px]">//</p>
                                        </div>
                                    ))}
                                </div>
                            ))
                        }

                    </motion.div>

                    <div className="absolute inset-0 z-10 bg-radial-[at_50%_50%] from-transparent to-black pointer-events-none to-90%"></div>

                </div>
            </div>

            <div className="flex flex-row items-center mx-[7.5px] mt-2.5">
                <Plus color="white" size={15}/>
                <div className="h-px grow bg-white mx-2"></div>
                <Plus color="white" size={15} />
            </div>

        </div>
    );

}