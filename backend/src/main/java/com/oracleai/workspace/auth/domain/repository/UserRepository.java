package com.oracleai.workspace.auth.domain.repository;

import com.oracleai.workspace.auth.domain.entity.User;
import com.oracleai.workspace.auth.domain.valueobject.Email;
import com.oracleai.workspace.auth.domain.valueobject.UserId;
import com.oracleai.workspace.auth.domain.valueobject.Username;

import java.util.Optional;

public interface UserRepository {
    Optional<User> findById(UserId id);
    Optional<User> findByUsername(Username username);
    Optional<User> findByEmail(Email email);
    boolean existsByUsername(Username username);
    boolean existsByEmail(Email email);
    User save(User user);
    void delete(User user);
}
