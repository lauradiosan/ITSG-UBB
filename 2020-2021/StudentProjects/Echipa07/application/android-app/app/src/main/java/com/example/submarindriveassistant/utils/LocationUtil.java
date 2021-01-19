package com.example.submarindriveassistant.utils;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;

public class LocationUtil extends Activity {
    private static LocationManager locationManager;
    MyLocationListenerGPS myLocationListenerGPS = new MyLocationListenerGPS();
    Location currentLocation = null;

    @SuppressLint("MissingPermission")
    public void updateLocationData(Context context){
        locationManager = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);
        locationManager.requestLocationUpdates(
                LocationManager.GPS_PROVIDER, 10, 0, myLocationListenerGPS);
        //locationManager.requestLocationUpdates( LocationManager.NETWORK_PROVIDER, 100, 10, myLocationListenerGPS);
    }

    public Location getLocation() {
       return currentLocation;
    }

    public class MyLocationListenerGPS implements LocationListener {
        @Override
        public void onLocationChanged(Location location) {
            currentLocation = location;
        }
    }
}