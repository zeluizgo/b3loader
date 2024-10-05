package com.jl.b3springboot.b3springboot;

import java.util.Date;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.Data;

@Data
@Document(collection="markets.b3.assets")
public class B3Asset {
    @Id String symbol;
    String description;
    double volume;
    double tickVolume;
    Date startTimestamp;
    Date finishTimestamp;
    String status;
}
