package com.dark.sail;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.EditText;

import com.dark.sailibrary.Sailboat;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    Sailboat sailboat;
    EditText et;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        et = (EditText) findViewById(R.id.et);
        Log.d("TAG", "onCreate: " + et.getHint().toString());
        ArrayList<Integer> arrayList = new ArrayList<>();

        arrayList.add(R.id.button);
        arrayList.add(R.id.text);
        arrayList.add(R.id.et);

        sailboat = new Sailboat();
        sailboat.initialize(MainActivity.this, arrayList);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        sailboat.destroy();
    }

    public void click(View view) {
        Log.d("TAG", "onCreate: " + et.getHint().toString());
    }
}
