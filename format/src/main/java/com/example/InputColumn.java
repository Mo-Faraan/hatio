package com.example;

import java.util.ArrayList;

public class InputColumn {
    private String columnName;
    private String headerName;
    private int orderId;
    private boolean isCustom;
    private String defaultValue;
    private String dateFormat; 

    
    public String getColumnName() {
        return columnName;
    }

    public void setColumnName(String columnName) {
        this.columnName = columnName;
    }

    public String getHeaderName() {
        return headerName;
    }

    public void setHeaderName(String headerName) {
        this.headerName = headerName;
    }

    public int getOrderId() {
        return orderId;
    }

    public void setOrderId(int orderId) {
        this.orderId = orderId;
    }

    public boolean isCustom() {
        return isCustom;
    }

    public void setCustom(boolean isCustom) {
        this.isCustom = isCustom;
    }

    public String getDefaultValue() {
        return defaultValue;
    }

    public void setDefaultValue(String defaultValue) {
        this.defaultValue = defaultValue;
    }

    public String getDateFormat() {
        return dateFormat;
    }

    public void setDateFormat(String dateFormat) {
        this.dateFormat = dateFormat;
    }

    @Override
    public String toString() {
        return "Column{" +
                "columnName='" + columnName + '\'' +
                ", headerName='" + headerName + '\'' +
                ", orderId=" + orderId +
                ", isCustom=" + isCustom +
                ", defaultValue='" + defaultValue + '\'' +
                ", dateFormat='" + dateFormat + '\'' +
                '}';
    }
    
}
