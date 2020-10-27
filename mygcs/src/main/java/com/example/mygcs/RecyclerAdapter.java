package com.example.mygcs;

import android.content.Context;
import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.ArrayList;

public class RecyclerAdapter extends RecyclerView.Adapter<RecyclerAdapter.ViewHolder>{

    ArrayList<RecyclerItem> messageBundle = new ArrayList<>();

    public RecyclerAdapter(ArrayList<RecyclerItem> bundle){
        this.messageBundle = bundle;
    }

    public class ViewHolder extends RecyclerView.ViewHolder{
        TextView textView;

        public ViewHolder(@NonNull View view) {
            super(view);
            textView = view.findViewById(R.id.message);
        }
    }

    @NonNull
    @Override
    public RecyclerAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        Context mContext = viewGroup.getContext();
        LayoutInflater inflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View itemView = inflater.inflate(R.layout.send_message_item,  viewGroup, false);//viewGroup는 각각의 아이템을 위해서 정의한 xml레이아웃의 최상위 레이아웃이다.
        RecyclerAdapter.ViewHolder holder = new RecyclerAdapter.ViewHolder(itemView);
        return holder;
    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerAdapter.ViewHolder viewHolder, int i) {
        RecyclerItem message = messageBundle.get(i); //리사이클러뷰에서 몇번쨰게 지금 보여야되는시점이다 알려주기위해
        viewHolder.textView.setText(message.getMessage());//그거를 홀더에넣어서 뷰홀더가 데이터를 알 수 있게되서 뷰홀더에 들어가있는 뷰에다가 데이터 설정할 수 있음
    }

    @Override
    public int getItemCount() {
        return messageBundle.size();
    }
}