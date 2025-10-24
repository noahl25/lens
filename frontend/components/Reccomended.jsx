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
                        reccomended.map((item, key) => (
                            <div key={key}>
                                <div className="w-full h-fit mb-5">
                                    <p className="text-4xl">Hello hello hello hello</p>
                                    <a href="https://www.google.com" target="_blank" className="text-white/50">https://www.google.com</a>
                                    {
                                        item.image ? <img src={item.image} className="w-[800px] mt-4 rounded-2xl border-2 border-white/70"/>
                                            :
                                        <p className="w-[500px] mt-4">{item.body}</p>
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