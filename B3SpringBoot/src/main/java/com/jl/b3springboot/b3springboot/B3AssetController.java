package com.jl.b3springboot.b3springboot;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.util.Date;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
public class B3AssetController {

    private final B3AssetRepository repository;

    public B3AssetController(B3AssetRepository repository) {
        this.repository = repository;
    }

    //Sample request: /registerb3asset?symbol=PETR4&volume=0.1&tickVolume=13.88&start_timestamp=2023-01-09 13:00:00&finish_timestamp=null&status=open
    @GetMapping("/registerb3asset")
    public Mono<B3Asset> putAsset(@RequestParam(required = true) String symbol,
                                @RequestParam(required = false) String description,
                                @RequestParam(required = false) double volume,
                                @RequestParam(required = false) double tickVolume,
                                @RequestParam(required = false, defaultValue = "") String start_timestamp,
                                @RequestParam(required = false, defaultValue = "") String finish_timestamp,
                                @RequestParam(required = false) String status) {

        Date datetime_start, datetime_finish;
        try {
            if(start_timestamp.equals(""))
            {
                datetime_start = Date.from(Instant.now());
            }
            else
            {
                SimpleDateFormat      sdf   = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
                datetime_start = sdf.parse(start_timestamp);
            }
        } catch (ParseException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            datetime_start = Date.from(Instant.now());
        }

        try {
            datetime_finish = null;
            if(!finish_timestamp.equals(""))
            {
                SimpleDateFormat      sdf   = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
                datetime_finish = sdf.parse(finish_timestamp);
            }
        } catch (ParseException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            datetime_finish = Date.from(Instant.now());
        }
                                    
        B3Asset ordem = new B3Asset();
        ordem.symbol = symbol;
        ordem.description = description;
        ordem.volume = volume;
        ordem.tickVolume = tickVolume;
        ordem.startTimestamp = datetime_start;
        ordem.finishTimestamp = datetime_finish;
        ordem.status = status;
        return repository.save(ordem);
    }
    

    @GetMapping("/b3assets")
    public Flux<B3Asset> listing() {
        return repository.findAll();
    }
}
