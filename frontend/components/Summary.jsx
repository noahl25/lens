import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import React from "react";
export default function Summary({ title, subtitle, text, cols }) {
    function Formatter({ text }) {
        const parts = text.split('**');

        return (
            <>
                {parts.map((part, index) => {
                    if (index % 2 === 1) {
                        return <strong key={index}>{part}</strong>;
                    } else {
                        return <React.Fragment key={index}>{part}</React.Fragment>;
                    }
                })}
            </>
        );
    }
    return <Card className={`pt-0 bg-black text-white border-white/20 border-2 col-span-${cols}`}>
        <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
            <div className="grid flex-1 gap-1">
                <CardTitle>{title}</CardTitle>
                <CardDescription>
                    {subtitle}
                </CardDescription>
            </div>
        </CardHeader>
        <CardContent className={"flex-1 flex justify-center items-center"}>
            <div className="">
                <Formatter text={text}/>
            </div>
        </CardContent >
    </Card >
}