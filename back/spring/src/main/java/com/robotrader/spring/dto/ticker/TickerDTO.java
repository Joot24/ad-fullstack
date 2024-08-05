package com.robotrader.spring.dto.ticker;

import com.robotrader.spring.model.enums.TickerTypeEnum;
import com.robotrader.spring.trading.dto.IPredictionServiceDTO;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class TickerDTO implements IPredictionServiceDTO {

    @Enumerated(EnumType.STRING)
    private TickerTypeEnum tickerType;

    @NotBlank
    private String tickerName;
}
