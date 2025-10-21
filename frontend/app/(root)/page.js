'use client'

import Threads from "@/components/Threads";
import Query from "@/components/Query";

export default function Home() {

	return (
		<div className="w-screen h-screen flex justify-center items-center bg-black relative bg-carbon">
			<Threads
				amplitude={1}
				distance={0.6}
				enableMouseInteraction={false}
				className="absolute inset-0"
			/>
			<Query/>
		</div>
	);
}
