import Header from "@/components/Header";
import Threads from "@/components/Threads";

export default function Home() {
	return (
		<>
			<Header/>
			<div className="w-screen h-screen flex justify-center items-center bg-black relative bg-carbon">
				<Threads
					amplitude={1}
					distance={0}
					enableMouseInteraction={false}
					className="absolute inset-0"
				/>
			</div>
		</>
	);
}
