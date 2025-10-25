'use client'

import { fontBasic } from "@/app/layout";
import { Search, X } from "lucide-react";
import { LineGraph } from "./LineGraph";
import DashboardTable from "./DashboardTable";
import Summary from "./Summary";
import DashboardRadial from "./DashboardRadial";
import Reccomended from "./Reccomended";
import { useState, useEffect, useRef, Fragment } from "react";
import { useApi } from "@/lib/api";
import { AnimatePresence, motion } from "motion/react";

export default function Dashboard({ query }) {

    const [components, setComponents] = useState(undefined);
    const [ready, setReady] = useState(false);
    const [error, setError] = useState(false);

    const getRemainingCols = (currentIndex, components) => {

        const totalCols = 3;
        let usedCols = 0;

        for (let i = 0; i < currentIndex; i++) {
            const c = components[i];
            const cols = c.cols || 1;
            usedCols += cols;
        }

        const remaining = usedCols % totalCols;
        if (remaining == 0) {
            if (components[currentIndex + 1])
                return 3 - components[currentIndex + 1].cols;
            return 2
        }
        else {
            return 3 - remaining
        }
    };

    const getComponent = (component, key, components) => {
        return (
            <>
                {(() => {
                    switch (component.type) {
                        case "radial":
                            return (
                                <DashboardRadial
                                    title={component.title}
                                    subtitle={component.subtitle}
                                    min={component.min}
                                    max={component.max}
                                    number={component.value}
                                    label={component.label}
                                    leftLabel={component.leftLabel}
                                    rightLabel={component.rightLabel}
                                    labelColor={component.color}
                                />
                            );

                        case "summary":
                            return (
                                <Summary
                                    title={component.title}
                                    subtitle={component.subtitle}
                                    text={component.text}
                                    cols={getRemainingCols(key, components)}
                                />
                            );

                        case "recommended":
                            return (
                                <Reccomended
                                    reccomended={component.recommended}
                                />
                            );

                        case "table":
                            return (
                                <DashboardTable
                                    title={component.title}
                                    subtitle={component.subtitle}
                                    headers={component.headers}
                                    data={component.data}
                                />
                            );

                        case "graph":
                            return (
                                <LineGraph
                                    title={component.title}
                                    subtitle={component.subtitle}
                                    data={component.data}
                                />
                            );

                        default:
                            console.error("Unknown component type:", component.type);
                            return null;
                    }
                })()}
            </>
        );
    };

    const inputRef = useRef();
    const onSubmit = () => {

        setReady(false);
        setComponents(undefined);
        setError(false);

        makeRequest("chat", {
            method: "POST",
            body: JSON.stringify({
                "request": inputRef.current.value
            })
        }).then((result) => {
            if ("result" in result) {
                if (!components) {
                    setReady(true);
                    setComponents(result.result);

                    console.log(result.result)
                }
            }
            else {
                setError(true);
            }
        })

    }

    const { makeRequest } = useApi();
    useEffect(() => {

        if (!ready) {
            makeRequest("chat", {
                method: "POST",
                body: JSON.stringify({
                    "request": query
                })
            }).then((result) => {
                if ("result" in result) {
                    if (!components) {
                        setReady(true);
                        setComponents(result.result);

                        console.log(result.result)
                    }
                }
                else {
                    setError(true);
                }
            })
        }

    }, []);

    return (
        <div className="w-full h-full pb-10 overflow-x-hidden">
            <div className={`mt-[85px] max-w-6xl mx-auto text-white ${fontBasic.className}`}>
                <div className="flex items-center justify-between gap-6 mb-5">
                    <div>
                        <h1 className="text-5xl">Dashboard</h1>
                        <p className="text-xs text-white/60 relative translate-x-[2px] mt-1">Explore your AI-powered results.</p>
                    </div>
                    <div>
                        <div className="w-[500px] h-12 rounded-4xl backdrop-blur-md border-2 border-white/50 relative flex">
                            <input ref={inputRef} placeholder={query} type="text" className="text-sm ml-12 mr-4 focus:outline-none w-full" onKeyDown={(e) => e.key === "Enter" && onSubmit()}></input>
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2" color="#ffffff74" />
                        </div>
                        <p className="text-xs text-center text-white/60 mt-2">Press Enter to search.</p>
                    </div>
                </div>
                <AnimatePresence mode="wait">

                    {
                        ready ?
                            <motion.div className="grid grid-flow-row-dense grid-cols-3 gap-10 auto-rows-min auto-flow-dense"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{
                                    duration: 1,
                                    ease: "easeInOut"
                                }}
                                exit={{
                                    opacity: 0
                                }}
                                key="grid"
                            >
                                {
                                    components.map((item, key) => {
                                        return <Fragment key={key}>
                                            {getComponent(item, key, components)}
                                        </Fragment>
                                        })
                                }
                            </motion.div>
                            :
                            <motion.div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/4 flex flex-col justify-center items-center" key="waiting"
                                initial={{
                                    opacity: 0
                                }}
                                animate={{
                                    opacity: 1
                                }}
                                exit={{
                                    opacity: 0,
                                    transition: {
                                        repeat: 0,
                                        duration: 1
                                    }
                                }}
                                transition={{
                                    repeat: Infinity,
                                    duration: 3,
                                    delay: 1,
                                    repeatType: "mirror",
                                    ease: "easeOut"
                                }}
                            >
                                <img src="eth.png" width={100} height={100} className="relative"></img>
                            </motion.div>
                    }
                </AnimatePresence>
            </div>
        </div>
    );
}