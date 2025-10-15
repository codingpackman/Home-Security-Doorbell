import express from "express";
import cors from "cors";
import records from "./routes/records.js";
import notifications from "./routes/notifications.js";

const PORT = process.env.PORT || 5050;
const app = express();

app.use(cors());
app.use(express.json());
app.use("/record", records);
app.use("/notification", notifications);

// start the express server
app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
})