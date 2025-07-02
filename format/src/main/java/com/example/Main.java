package com.example;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
public class Main {

    private static Set<String> REQUIRED_KEYS = new HashSet<>(Arrays.asList("columnName", "headerName", "orderId", "isCustom", "defaultValue"));
    private static Set<String> OPTIONAL_KEYS = new HashSet<>(Arrays.asList("dateFormat"));

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String json = sc.nextLine();

        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode root = mapper.readTree(json);


            for (JsonNode node : root) {
                Set<String> keys = new HashSet<>();
                node.fieldNames().forEachRemaining(keys::add);

                if (!keys.containsAll(REQUIRED_KEYS)) {
                    System.out.println("Missing required keys: " + REQUIRED_KEYS + " in node: " + node);
                    return;
                }

                for (String key : keys) {
                    if (!REQUIRED_KEYS.contains(key) && !OPTIONAL_KEYS.contains(key)) {
                        System.out.println("Unknown key: " + key + " in node: " + node);
                        return;
                    }
                }
                if(!node.get("orderId").isInt()){
                    System.out.println("Invalid orderId type should be integer"+ " at node : "+node);
                    return;
                }
                if(!node.get("isCustom").isBoolean()){
                    System.out.println("Invalid isCustom type should be boolean"+ " at node : "+node);
                    return;
                }
            }
            System.out.println("JSON Input is VALID");
        } catch (Exception e) {
            System.out.println("Invalid JSON syntax " + e.getMessage());
        }finally{
            sc.close();
        }
    }
}

   
