package com.oracleai.workspace;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class OracleAiWorkspaceApplication {

    public static void main(String[] args) {
        SpringApplication.run(OracleAiWorkspaceApplication.class, args);
    }
}
