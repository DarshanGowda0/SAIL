package com.dark.sailibrary;

import android.app.Activity;
import android.support.annotation.NonNull;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by Rohan on 9/17/2016.
 */
public class Sailboat {

    FirebaseDatabase database;
    DatabaseReference databaseReference;
    Activity activity;
    ArrayList<ViewObject> listOfIds;
    String TAG = "Test";


    public Sailboat() {

        database = FirebaseDatabase.getInstance();
        databaseReference = database.getReference();

    }

    public void initialize(Activity activity, ArrayList<ViewObject> listOfIds) {
        this.activity = activity;
        this.listOfIds = listOfIds;

        sendInfo();

    }

    private void sendInfo() {

        String packageName = activity.getPackageName().replaceAll("\\.", "_");
        String activityName = activity.getClass().getSimpleName();

        Log.d(TAG, "sendInfo: " + activityName);

        HashMap<String, HashMap<String, String>> views = new HashMap<>();

        for (int i = 0; i < listOfIds.size(); i++) {
            View v = (activity.findViewById(listOfIds.get(i).id));
            String text;
            try {
                text = ((TextView) v).getHint().toString();
            } catch (Exception e) {
                text = ((TextView) v).getText().toString();
                e.printStackTrace();
            }

            Log.d(TAG, "sendInfo: id " + listOfIds.get(i).id);
            Log.d(TAG, "sendInfo: text " + text);
            HashMap<String, String> hash = new HashMap<>();
            hash.put("hint", text);
            views.put("" + listOfIds.get(i).id, hash);
        }

        HashMap<String, Object> activityHash = new HashMap<>();
        activityHash.put("views", views);

        HashMap<String, Object> packageHash = new HashMap<>();
        packageHash.put(activityName, activityHash);

//        HashMap<String,Object> rootHash = new HashMap<>();
//        rootHash.put("activities",packageHash);
//        packageHash.put("temp","HEllo");


        databaseReference.child("packages/" + packageName + "/activities").setValue(packageHash)
                .addOnSuccessListener(new OnSuccessListener<Void>() {
                    @Override
                    public void onSuccess(Void aVoid) {
                        Log.d("TAG", "onSuccess: ");

                    }
                }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Log.d("TAG", "onFailure: " + e);
            }
        });

    }


}
