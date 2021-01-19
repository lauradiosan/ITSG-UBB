package com.example.submarindriveassistant.utils;

import android.content.Context;
import android.graphics.Color;
import android.location.Location;
import android.os.Build;
import android.util.Log;
import android.widget.TextView;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.submarindriveassistant.MainActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.Timer;
import java.util.TimerTask;

public class SpeedUtil extends AppCompatActivity {
    private static Location oldLocation = null;
    private static LocationUtil locationUtil = null;
    private static boolean showSpeed = true;
    private static long time = 0 ;

    public void startShowingSpeed(Context context, TextView textView, LocationUtil defaultLocationUtil) {
        this.locationUtil = defaultLocationUtil;
        Timer T = new Timer();
        T.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        time++;
                    }
                });
            }
        }, 0, 10);
        new Thread(new Runnable() {
            public void run() {
                while (showSpeed) {
                    if (locationUtil != null) {
                        Location newLocation = locationUtil.getLocation();
                        if (oldLocation == null && newLocation != null) {
                            oldLocation = locationUtil.getLocation();
                        } else {
                            if (newLocation != null) {
                                long distance = calculateDistance(oldLocation.getLatitude(),
                                        oldLocation.getLongitude(),
                                        newLocation.getLatitude(),
                                        newLocation.getLongitude());
                                if (distance >= 1) {
                                    if (time != 0) {
                                        long speed = (distance * 3600* 100)/(time * 1000);
                                        if(speed<50){
                                            textView.setTextColor(Color.BLACK);
                                        }else if(speed < 80){
                                            textView.setTextColor(Color.parseColor("#fc5e03"));
                                        }else{
                                            textView.setTextColor(Color.RED);
                                        }
                                        textView.setText("Your speed :\n" + speed + " km/h");
                                        time = 0;
                                        oldLocation = newLocation;
                                    }
                                }

                            }
                        }
                    }else {
                        locationUtil = MainActivity.getLocationUtil();
                    }
                }
            }
        }).start();


    }

    private static long calculateDistance(double lat1, double lng1, double lat2, double lng2) {
        double dLat = Math.toRadians(lat2 - lat1);
        double dLon = Math.toRadians(lng2 - lng1);
        double a = Math.sin(dLat / 2) * Math.sin(dLat / 2)
                + Math.cos(Math.toRadians(lat1))
                * Math.cos(Math.toRadians(lat2)) * Math.sin(dLon / 2)
                * Math.sin(dLon / 2);
        double c = 2 * Math.asin(Math.sqrt(a));
        long distanceInMeters = Math.round(6371000 * c);
        return distanceInMeters;
    }
}