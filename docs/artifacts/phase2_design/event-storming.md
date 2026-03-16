# Event Storming - Oracle AI Data Visualizer

## 1. Actors
| Actor | Type | Description |
|-------|------|-------------|
| BusinessUser | User | Người dùng không có kiến thức kỹ thuật, muốn xem ERD và query dữ liệu |
| DataAnalyst | User | Người dùng nâng cao, muốn phân nhóm dữ liệu và phân tích |
| Developer | User | Người dùng kỹ thuật, muốn sync Vector DB và build AI apps |
| DBA | User | Người quản trị, giám sát schema và sync |
| OllamaService | System | AI service cho Text-to-SQL và embeddings |
| ChromaDBService | System | Vector database cho semantic search |
| OracleDatabase | System | Oracle Database nguồn |

## 2. Commands
| Command | Actor | Trigger |
|---------|-------|---------|
| ConnectToDatabase | BusinessUser | Nhập connection details |
| ViewSchema | BusinessUser | Click "View ERD" |
| AskQuestion | BusinessUser | Nhập câu hỏi bằng tiếng Việt/Anh |
| CreateGroup | DataAnalyst | Click "Create Group" |
| AssignTableToGroup | DataAnalyst | Drag table vào group |
| StartFullSync | Developer | Click "Start Full Sync" |
| StartIncrementalSync | Developer | Click "Start Incremental Sync" |
| SearchVectors | Developer | Gọi API search |
| RegisterUser | BusinessUser | Đăng ký tài khoản |
| LoginUser | BusinessUser | Đăng nhập |

## 3. Domain Events
| Event | Type | Cause | Effect |
|-------|------|-------|--------|
| DatabaseConnected | Domain | User kết nối DB thành công | Hiển thị success, enable features |
| ConnectionFailed | Domain | Kết nối DB thất bại | Hiển thị error message |
| SchemaExtracted | Domain | Metadata extraction hoàn tất | ERD diagram rendered |
| ERDRendered | Domain | Diagram đã render | User có thể tương tác |
| SQLGenerated | Domain | Ollama trả về SQL | Hiển thị SQL cho user review |
| SQLExecuted | Domain | SQL chạy thành công | Hiển thị results table |
| SQLExecutionFailed | Domain | SQL lỗi | Hiển thị error |
| GroupCreated | Domain | User tạo group mới | Group hiển thị trong sidebar |
| TableAssignedToGroup | Domain | User assign table | Table xuất hiện trong group |
| SyncStarted | Domain | User click sync | Progress bar hiển thị |
| DataEmbedded | Domain | Embedding generation hoàn tất | Vector stored in ChromaDB |
| SyncCompleted | Domain | Sync hoàn tất | Success notification |
| SyncFailed | Domain | Sync lỗi | Error notification với reason |
| VectorSearchCompleted | Domain | Search hoàn tất | Return results với scores |
| UserRegistered | Domain | Registration thành công | Tạo user record |
| UserLoggedIn | User | Login thành công | Return JWT token |

## 4. Process Flows

### Flow 1: Connect & View ERD
```
ConnectToDatabase → DatabaseConnected 
    → SchemaExtracted → ERDRendered
```

### Flow 2: Natural Language Query
```
AskQuestion → SQLGenerated 
    → SQLExecuted → QueryResultsReturned
    (OR)
    → SQLExecutionFailed → ErrorDisplayed
```

### Flow 3: Data Grouping
```
CreateGroup → GroupCreated 
    → AssignTableToGroup → TableAssignedToGroup
```

### Flow 4: Vector Sync
```
StartFullSync → SyncStarted 
    → DataExtracted → DataEmbedded → SyncCompleted
    (OR)
    → SyncFailed → ErrorDisplayed
```

### Flow 5: Authentication
```
RegisterUser → UserRegistered → UserLoggedIn
LoginUser → UserLoggedIn → JWTIssued
```

## 5. Timeline View
```
[User Login] → [Database Connect] → [Schema Extract] → [ERD Render]
                                                            ↓
                                              [Natural Language Query]
                                                            ↓
                                              [Vector Sync (optional)]
                                                            ↓
                                              [Semantic Search (optional)]
```
