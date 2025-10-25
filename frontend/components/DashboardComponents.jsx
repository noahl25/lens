'use client'

import { Computer } from "lucide-react";
import { Fragment } from "react";
import { AnimatePresence, motion } from "motion/react";
import { useEffect, useState } from "react";
import DashboardRadial from "./DashboardRadial";
import Summary from "./Summary";
import Reccomended from "./Reccomended";
import DashboardTable from "./DashboardTable";
import { LineGraph } from "./LineGraph";
import { useApi } from "@/lib/api";

export default function DashboardComponents() {

    const [components, setComponents] = useState(undefined);
    const [ready, setReady] = useState(false);
    const [error, setError] = useState(false);

    const getComponent = (component, key) => {
        return (
            <motion.div
                key={key}
                initial={{ opacity: 0, y: 25 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -25 }}
                transition={{ duration: 1, ease: "easeOut", delay: 0.25 * (key + 1) }}
                className={`col-span-${component.cols}`}
            >
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
                                />
                            );

                        case "recommended":
                            return (
                                <Reccomended
                                    reccomended={component.reccomended}
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
            </motion.div>
        );
    };

    const { makeRequest } = useApi();
    useEffect(() => {

        makeRequest("chat", {
            method: "POST",
            body: JSON.stringify({
                "request": "bitcoin price now"
            })
        }).then((result) => {
            if ("result" in result) {
                setReady(true);
                setComponents(result.result);
            }
            else {
                setError(true);
            }
        })

    }, []);

    return (
        <AnimatePresence mode="wait">
                  
            {
                error ? <div className="absolute left-1/2 top-1/3 text-white">An error occurred. Please try again.</div>
                    :
                    ready ? 
                        <>
                            {
                                components.map((item, key) => (
                                    <Fragment key={key}>
                                        {
                                            getComponent(item, key)
                                        }
                                    </Fragment>
                                ))
                            }
                        </>
                        :
                    <motion.div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/4 flex flex-col justify-center items-center"
                        initial={{
                            opacity: 0
                        }}
                        animate={{
                            opacity: 1
                        }}
                        exit={{
                            opacity: 0
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
    );
}