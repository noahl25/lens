import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

export default function Reccomended({ reccomended }) {
    return (
        <Card className="pt-0 bg-black text-white border-white/20 border-2 col-span-2 h-[400px]">
            <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
                <div className="grid flex-1 gap-1">
                    <CardTitle>Reccommended</CardTitle>
                    <CardDescription>
                        Some places to learn more.
                    </CardDescription>
                </div>
            </CardHeader>
            <CardContent className="overflow-y-scroll h-full dark-scrollbar">
                <div className="flex items-center justify-center flex-col px-5 gap-2 pt-3">
                    {
                        reccomended.slice(0, 5).map((item, key) => (
                            <div key={key}>
                                <div className="w-full h-fit mb-5">
                                    <p className="text-4xl">{item.title}</p>
                                    <a href={item.url} target="_blank" className="text-white/50">{item.url.length > 30 ? `${item.url.slice(0, 30)}...` : item.url}</a>
                                    {
                                        <p className="w-[600px] mt-4">{item.content.length > 350 ? `${item.content.slice(0, 350)}...` : item.content} </p>
                                    }
                                </div>
                                <div className="w-full h-[2px] bg-white mt-4 mb-2"/>
                            </div>

                        ))
                    }
                </div>
            </CardContent>
        </Card>
    )
}