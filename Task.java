import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class TaskManager {

    private final Map<String, Task> tasks = new HashMap<>();

    public String createTask(String title, String description) {
        if (title == null || title.isBlank()) {
            throw new IllegalArgumentException("Title cannot be empty");
        }

        String id = UUID.randomUUID().toString();
        Task task = new Task(id, title, description);
        tasks.put(id, task);

        return id;
    }

    public boolean completeTask(String id) {
        Task task = tasks.get(id);

        if (task == null) {
            return false;
        }

        task.setCompleted(true);
        task.setCompletedAt(LocalDateTime.now());
        return true;
    }

    public boolean deleteTask(String id) {
        if (!tasks.containsKey(id)) {
            return false;
        }

        tasks.remove(id);
        return true;
    }

    public Task findTask(String id) {
        return tasks.get(id);
    }

    public List<Task> getAllTasks() {
        return new ArrayList<>(tasks.values());
    }

    public List<Task> getCompletedTasks() {
        List<Task> completed = new ArrayList<>();

        for (Task task : tasks.values()) {
            if (task.isCompleted()) {
                completed.add(task);
            }
        }

        return completed;
    }

    public List<Task> getPendingTasks() {
        List<Task> pending = new ArrayList<>();

        for (Task task : tasks.values()) {
            if (!task.isCompleted()) {
                pending.add(task);
            }
        }

        return pending;
    }

    public int countCompletedTasks() {
        int count = 0;

        for (Task task : tasks.values()) {
            if (task.isCompleted()) {
                count++;
            }
        }

        return count;
    }

    public int countPendingTasks() {
        int count = 0;

        for (Task task : tasks.values()) {
            if (!task.isCompleted()) {
                count++;
            }
        }

        return count;
    }

    public boolean updateTitle(String id, String newTitle) {
        Task task = tasks.get(id);

        if (task == null || newTitle == null || newTitle.isBlank()) {
            return false;
        }

        task.setTitle(newTitle);
        return true;
    }

    public boolean updateDescription(String id, String description) {
        Task task = tasks.get(id);

        if (task == null) {
            return false;
        }

        task.setDescription(description);
        return true;
    }

    public void markAllCompleted() {
        for (Task task : tasks.values()) {
            task.setCompleted(true);
            task.setCompletedAt(LocalDateTime.now());
        }
    }

    public void clearCompletedTasks() {
        List<String> idsToRemove = new ArrayList<>();

        for (Task task : tasks.values()) {
            if (task.isCompleted()) {
                idsToRemove.add(task.getId());
            }
        }

        for (String id : idsToRemove) {
            tasks.remove(id);
        }
    }

    public String generateSummary() {
        int total = tasks.size();
        int completed = countCompletedTasks();
        int pending = countPendingTasks();

        StringBuilder summary = new StringBuilder();
        summary.append("Task Summary\n");
        summary.append("----------------\n");
        summary.append("Total: ").append(total).append("\n");
        summary.append("Completed: ").append(completed).append("\n");
        summary.append("Pending: ").append(pending).append("\n");

        return summary.toString();
    }

    public Map<String, Integer> getStatistics() {
        Map<String, Integer> statistics = new HashMap<>();

        statistics.put("total", tasks.size());
        statistics.put("completed", countCompletedTasks());
        statistics.put("pending", countPendingTasks());

        return statistics;
    }

    public void printTasks() {
        if (tasks.isEmpty()) {
            System.out.println("No tasks available.");
            return;
        }

        for (Task task : tasks.values()) {
            System.out.println(formatTask(task));
        }
    }

    private String formatTask(Task task) {
        String status = task.isCompleted() ? "DONE" : "PENDING";

        return String.format(
                "[%s] %s - %s",
                status,
                task.getTitle(),
                task.getDescription()
        );
    }

    public boolean containsTask(String id) {
        return id != null && tasks.containsKey(id);
    }

    public void renamePendingTasks(String prefix) {
        if (prefix == null) {
            return;
        }

        for (Task task : tasks.values()) {
            if (!task.isCompleted()) {
                task.setTitle(prefix + task.getTitle());
            }
        }
    }

    public List<String> search(String keyword) {
        List<String> results = new ArrayList<>();

        if (keyword == null || keyword.isBlank()) {
            return results;
        }

        String query = keyword.toLowerCase();

        for (Task task : tasks.values()) {
            String title = task.getTitle().toLowerCase();
            String description = task.getDescription().toLowerCase();

            if (title.contains(query) || description.contains(query)) {
                results.add(task.getId());
            }
        }

        return results;
    }

    public static class Task {
        private final String id;
        private String title;
        private String description;
        private boolean completed;
        private LocalDateTime createdAt;
        private LocalDateTime completedAt;

        public Task(String id, String title, String description) {
            this.id = id;
            this.title = title;
            this.description = description == null ? "" : description;
            this.completed = false;
            this.createdAt = LocalDateTime.now();
        }

        public String getId() {
            return id;
        }

        public String getTitle() {
            return title;
        }

        public void setTitle(String title) {
            this.title = title;
        }

        public String getDescription() {
            return description;
        }

        public void setDescription(String description) {
            this.description = description;
        }

        public boolean isCompleted() {
            return completed;
        }

        public void setCompleted(boolean completed) {
            this.completed = completed;
        }

        public LocalDateTime getCreatedAt() {
            return createdAt;
        }

        public LocalDateTime getCompletedAt() {
            return completedAt;
        }

        public void setCompletedAt(LocalDateTime completedAt) {
            this.completedAt = completedAt;
        }

        @Override
        public String toString() {
            return "Task{" +
                    "id='" + id + '\'' +
                    ", title='" + title + '\'' +
                    ", completed=" + completed +
                    ", createdAt=" + createdAt +
                    '}';
        }
    }
}
