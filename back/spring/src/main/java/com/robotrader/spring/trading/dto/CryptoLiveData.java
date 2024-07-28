package com.robotrader.spring.trading.dto;

import lombok.Data;
import lombok.ToString;

@Data
@ToString(callSuper = true)
public class CryptoLiveData extends LiveMarketData {
    private String pair; // Crypto pair
}
