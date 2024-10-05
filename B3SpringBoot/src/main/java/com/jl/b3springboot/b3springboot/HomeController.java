package com.jl.b3springboot.b3springboot;


import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;



@RestController
public class HomeController {

    @GetMapping
    public String greeting(@RequestParam(required = false, defaultValue = "") String name) {

        return name.equals("") ? "Hey!" : "Hey," + name + "!";
        
    }
    
}
