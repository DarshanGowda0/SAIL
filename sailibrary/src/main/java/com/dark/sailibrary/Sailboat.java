package com.dark.sailibrary;

import android.app.Activity;
import android.view.View;
import android.widget.Button;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.ArrayList;

/**
 * Created by Rohan on 9/17/2016.
 */
public class Sailboat {

    FirebaseDatabase database;
    DatabaseReference databaseReference;
    Activity activity;
    ArrayList<ViewObject> listOfIds;


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

        String packageName = activity.getPackageName().replaceAll("\\.","_");
        String activityName = activity.getApplicationContext().getClass().getSimpleName();
        for(int i=0;i<listOfIds.size();i++){
            View v = (activity.findViewById(listOfIds.get(i).id));
//            Object button = (listOfIds.get(i).aClass) v;
//            button.getText();
        }

    }


}
