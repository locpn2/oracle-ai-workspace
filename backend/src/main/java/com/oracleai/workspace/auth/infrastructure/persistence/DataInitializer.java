package com.oracleai.workspace.auth.infrastructure.persistence;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.oracleai.workspace.auth.domain.entity.User;
import com.oracleai.workspace.auth.domain.repository.UserRepository;
import com.oracleai.workspace.auth.domain.valueobject.Email;
import com.oracleai.workspace.auth.domain.valueobject.HashedPassword;
import com.oracleai.workspace.auth.domain.valueobject.Role;
import com.oracleai.workspace.auth.domain.valueobject.UserId;
import com.oracleai.workspace.auth.domain.valueobject.Username;

import java.util.Set;

@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner initUsers(UserRepository userRepository) {
        return args -> {
            Username adminUsername = new Username("admin");
            if (!userRepository.existsByUsername(adminUsername)) {
                User admin = User.builder()
                        .id(UserId.generate())
                        .username(adminUsername)
                        .email(new Email("admin@example.com"))
                        .password(HashedPassword.fromPlain("Admin123"))
                        .roles(Set.of(Role.ADMIN))
                        .build();
                userRepository.save(admin);
                System.out.println("Default admin user created: admin / admin123");
            }
        };
    }
}
