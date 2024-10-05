package com.jl.b3springboot.b3springboot;
/* 
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration; */
import org.springframework.data.mongodb.repository.config.EnableReactiveMongoRepositories;

//import reactor.core.publisher.Flux;

@EnableReactiveMongoRepositories
public class LoadDatabase {

/*     @Bean
    CommandLineRunner init (PredictRepository repository) {
        return args -> { */
/*             Flux.just(
                      new Chapter("Quick Start with Java!"),
                      new Chapter("Reactive Web with Spring Boot"),
                      new Chapter("...and more!"))
                      .flatMap(repository::save)
                      .subscribe(System.out::println); */

/*         };
    } */
    
}
