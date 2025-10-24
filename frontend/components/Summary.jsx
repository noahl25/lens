import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

export default function Summary({ title, subtitle, text }) {
    return <Card className="pt-0 bg-black text-white border-white/20 border-2 col-span-2">
        <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
            <div className="grid flex-1 gap-1">
                <CardTitle>{title}</CardTitle>
                <CardDescription>
                    {subtitle}
                </CardDescription>
            </div>
        </CardHeader>
        <CardContent>
            <div>
                {text}
            </div>
        </CardContent >
    </Card >
}