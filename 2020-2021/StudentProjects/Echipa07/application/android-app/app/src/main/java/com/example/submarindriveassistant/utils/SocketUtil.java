package com.example.submarindriveassistant.utils;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.RequestQueue;
import com.example.submarindriveassistant.MainActivity;
import com.example.submarindriveassistant.R;
import com.github.nkzawa.emitter.Emitter;
import com.github.nkzawa.engineio.client.Transport;
import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Manager;
import com.github.nkzawa.socketio.client.Socket;

import org.json.JSONException;
import org.json.JSONObject;

import java.net.URISyntaxException;
import java.util.LinkedList;
import java.util.Queue;

public class SocketUtil extends AppCompatActivity {
    private static final String SERVER_URL = "http://10.0.2.2:8000/";
    private static Socket mSocket;
    private static boolean isConnectionWithSocketPossible = false;
    private static Queue<JSONObject> receivedMessagesQueue
            = new LinkedList<>();

    public SocketUtil() {
        try {
            mSocket = IO.socket(SERVER_URL);
            mSocket.connect();
        } catch (URISyntaxException e) {
            System.out.println("Couldn't connect to the server: " + e.getMessage());
        }

        mSocket.on("socket_connected", new Emitter.Listener() {
            @Override
            public void call(final Object... args) {
                isConnectionWithSocketPossible = true;

            }
        });
        mSocket.on("message_from_server", new Emitter.Listener() {
            @Override
            public void call(final Object... args) {
                JSONObject jsnobject = null;
                jsnobject = (JSONObject) args[0];
                String response = jsnobject.toString();
                response = response.substring(0, Math.min(response.length(), 100));
                System.out.println("Got response"+ response);
                receivedMessagesQueue.add(jsnobject);
            }
        });

    }

    public static boolean sendViaSocket(JSONObject jsonObject) {
        if (isConnectionWithSocketPossible) {
            if (mSocket.connected()) {
                System.out.println("Sending:\n" + jsonObject.toString());
                mSocket.emit("send_camera", jsonObject);
                return true;
            } else {
                return false;
            }
        }
        return false;
    }

    private static boolean isResponseReady() {
        return !receivedMessagesQueue.isEmpty();
    }

    public static JSONObject getResponse() {
        if (isConnectionWithSocketPossible) {
            // Ildiko: This sometimes crashes the app. If there is no response this will be a infinite loop. This is why we have sockets, we shouldn't have these loops, this is why we have the emitters! This should somehow change the view, not the view ask for this response
            while (!isResponseReady()) {
            }
            JSONObject response = receivedMessagesQueue.peek();
            receivedMessagesQueue.remove();
            return response;
        }
        return null;
    }
}
