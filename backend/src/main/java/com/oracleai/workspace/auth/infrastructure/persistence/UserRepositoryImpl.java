package com.oracleai.workspace.auth.infrastructure.persistence;

import com.oracleai.workspace.auth.domain.entity.User;
import com.oracleai.workspace.auth.domain.repository.UserRepository;
import com.oracleai.workspace.auth.domain.valueobject.Email;
import com.oracleai.workspace.auth.domain.valueobject.UserId;
import com.oracleai.workspace.auth.domain.valueobject.Username;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public class UserRepositoryImpl implements UserRepository {

    // In-memory storage for development - replace with JPA repository in production
    private final java.util.Map<UUID, UserEntity> users = new java.util.concurrent.ConcurrentHashMap<>();

    @Override
    public Optional<User> findById(UserId id) {
        UserEntity entity = users.get(id.value());
        return Optional.ofNullable(entity).map(UserEntity::toDomain);
    }

    @Override
    public Optional<User> findByUsername(Username username) {
        return users.values().stream()
                .filter(u -> u.getUsername().equals(username.value()))
                .findFirst()
                .map(UserEntity::toDomain);
    }

    @Override
    public Optional<User> findByEmail(Email email) {
        return users.values().stream()
                .filter(u -> u.getEmail().equals(email.value()))
                .findFirst()
                .map(UserEntity::toDomain);
    }

    @Override
    public boolean existsByUsername(Username username) {
        return users.values().stream()
                .anyMatch(u -> u.getUsername().equals(username.value()));
    }

    @Override
    public boolean existsByEmail(Email email) {
        return users.values().stream()
                .anyMatch(u -> u.getEmail().equals(email.value()));
    }

    @Override
    public User save(User user) {
        UserEntity entity = UserEntity.fromDomain(user);
        users.put(user.getId().value(), entity);
        return user;
    }

    @Override
    public void delete(User user) {
        users.remove(user.getId().value());
    }
}
