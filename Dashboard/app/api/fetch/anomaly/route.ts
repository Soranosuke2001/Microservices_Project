export async function GET() {
    try {
        const response = await fetch(process.env.ANOMALY_URL!)

        if (!response.ok) {
            return new Response(
                JSON.stringify({ message: "There was an error fetching data from Anomaly Detector Service"}),
                { status: 500 }
            )
        }

        const data = await response.json()

        if (!data) {
            return new Response(
                JSON.stringify("There was no data returned from the Anomaly Detector Service"),
                { status: 500 }
            )
        }

        return new Response(JSON.stringify({ message: data }), { status: 200 })
    } catch (err) {
        return new Response(
            JSON.stringify({ message: "There was an error fetching data"}),
            { status: 500 }
        )
    }
}