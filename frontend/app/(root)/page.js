'use client'

import Threads from "@/components/Threads";
import Query from "@/components/Query";
import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import Dashboard from "@/components/Dashboard";

export default function Home() {

	const [query, setQuery] = useState("");
	const [querySubmitted, setQuerySubmitted] = useState(false);

	useEffect(() => {

		if (query && query.length !== 0)
			setQuerySubmitted(true);

	}, [query]);

	return (
		<div className="overflow-x-hidden">
			<div className="absolute inset-0 bg-black -z-100"></div>
			<AnimatePresence mode="wait">
				{!querySubmitted ? (
					<motion.div
						key="query"
						exit={{ opacity: 0 }}
						transition={{ duration: 0.8 }}
						className="w-screen h-screen flex justify-center items-center bg-black relative overflow-y-hidden"
					>
						<Threads
							amplitude={1}
							distance={0.6}
							enableMouseInteraction={false}
							className="absolute inset-0 z-1 pointer-events-none"
						/>
						<Query setQuery={setQuery} />
					</motion.div>
				) : (
					<motion.div
						key="dashboard"
						initial={{ opacity: 0 }}
						animate={{ opacity: 1 }}
						exit={{ opacity: 0 }}
						transition={{ duration: 0.8 }}
						className="overflow-x-hidden"
					>
						<Dashboard query={query} />
					</motion.div>
				)}
			</AnimatePresence>

		</div>
	);
}
