package com.example.submarindriveassistant.utils;

import android.content.Context;
import android.graphics.Color;
import android.location.Location;
import android.os.Build;
import android.os.Bundle;
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
import com.example.submarindriveassistant.R;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class WeatherUtil extends AppCompatActivity {
    private static RequestQueue queue;
    private final String supersecretAPIKey = "47ed4a2dc283134c35f93f674b0f4949";

    public static void createRequestQueue(){
        queue = Volley.newRequestQueue(MainActivity.getContext());
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    public void setWeatherData(Context context, Location location, TextView textView) {

        String URL = "http://api.openweathermap.org/data/2.5/weather?lat="+location.getLatitude()+"&lon="+location.getLongitude()+"&units=metric"+"&appid="+supersecretAPIKey;
        textView.setText("");
        StringRequest request = new StringRequest(Request.Method.GET, URL, new Response.Listener<String>() {
                @Override
                public void onResponse(String response) {
                    try {
                        String screenText = "";
                        JSONObject jsnobject = new JSONObject(response);
                        screenText+=jsnobject.getString("name")+"\n";
                        JSONArray weatherTypeJSONArray = jsnobject.getJSONArray("weather");
                        JSONObject weatherTypeJSONObject = (JSONObject) weatherTypeJSONArray.get(0);
                        screenText+="Weather type: "+weatherTypeJSONObject.getString("main")+"\n";
                        JSONObject tempJSONObject = jsnobject.getJSONObject("main");
                        screenText+="Temp: "+tempJSONObject.getString("temp")+" C"+"\n";
                        if(Double. parseDouble(tempJSONObject.getString("temp")) <0d){
                            screenText+="Warning:\nPossible ICE on road.";
                            textView.setTextColor(Color.RED);
                        }else{
                            textView.setTextColor(Color.BLACK);
                        }
                        textView.setText(screenText);
                    } catch (JSONException e) {
                        textView.setText("JSON Exception please contact the devs for a fix :/");
                        e.printStackTrace();
                    }


                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    textView.setText("Cannot get weather data, please check you connection.");
                }
            });
            queue.add(request);
    }
}
