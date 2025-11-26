import express from "express";
import db from "../database/connection.js";
import { ObjectId } from "mongodb";
import { verifyToken } from "../middleware/auth.js";

const router = express.Router();

// Get all notifications for the logged-in user's doorbellID
router.get("/", verifyToken, async (req, res) => {
    try {
        const collection = db.collection("notifications");
        const notifications = await collection
            .find({ doorbellID: req.user.doorbellID })
            .sort({ createdAt: -1 }) // Sort by most recent
            .toArray();

        res.status(200).json(notifications);
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Error fetching notifications" });
    }
});

// Create a new notification
router.post("/", verifyToken, async (req, res) => {
    try {
        const { notificationType, dateTime, recordingPath } = req.body;

        const newNotification = {
            notificationType,
            dateTime,
            recordingPath,
            doorbellID: req.user.doorbellID,
            createdAt: new Date(),
        };

        const collection = db.collection("notifications");
        const result = await collection.insertOne(newNotification);

        res.status(201).json({ message: "Notification created", id: result.insertedId });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Error creating notification" });
    }
});

// Delete a notification by ID
router.delete("/:id", verifyToken, async (req, res) => {
    try {
        const collection = db.collection("notifications");
        const result = await collection.deleteOne({
            _id: new ObjectId(req.params.id),
            doorbellID: req.user.doorbellID, // Ensure the user owns the notification
        });

        if (result.deletedCount === 0) {
            return res.status(404).json({ message: "Notification not found" });
        }

        res.status(200).json({ message: "Notification deleted" });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Error deleting notification" });
    }
});

export default router;