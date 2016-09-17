package com.dark.sail;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;

import com.dark.sailibrary.Sailboat;
import com.dark.sailibrary.ViewObject;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ArrayList<ViewObject> arrayList = new ArrayList<>();

        arrayList.add(new ViewObject(Button.class,R.id.button));
        arrayList.add(new ViewObject(TextView.class,R.id.text));

        Sailboat sailboat = new Sailboat();
        sailboat.initialize(MainActivity.this,arrayList);
    }
}
